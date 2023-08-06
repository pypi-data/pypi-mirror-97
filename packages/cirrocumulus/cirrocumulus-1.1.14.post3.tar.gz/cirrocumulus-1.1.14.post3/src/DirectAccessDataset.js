import {isArray} from 'lodash';
import {getPassingFilterIndices} from './dataset_filter';
import {SlicedVector} from './SlicedVector';
import {Vector} from './Vector';
import {cacheValues, computeDerivedStats, getBasis, getTypeToMeasures, splitDataFilter} from './VectorUtil';


export class DirectAccessDataset {

    init(id, url) {
        this.id = id;
        this.key2data = {};
        this.format = "json";
        this.schema = null;
        if (this.url.endsWith(".jsonl") || this.url.endsWith(".jsonl.gz")) {
            this.format = "jsonl";
        }
        if (this.format === 'json' && !url.endsWith('.json') && !url.endsWith('.json.gz')) {
            url = url + 'schema.json';
        }
        this.url = url;
        this.baseUrl = this.url.substring(0, this.url.lastIndexOf('/') + 1);
        return Promise.resolve();
    }


    getByteRange(key) {
        let range = this.key2bytes[key];
        if (!range) {
            throw new Error(key + ' not found');
        }
        return {headers: {'Range': 'bytes=' + range[0] + '-' + range[1]}};
    }

    _fetch(key) {
        return this.format === 'json' ? fetch(this.baseUrl + key + '.json').then(r => r.json()) : fetch(this.url, this.getByteRange(key)).then(r => r.json());
    }

    fetchData(keys) {
        let promises = [];
        keys.forEach(key => {
            if (this.key2data[key] == null && key !== '__count') {
                let p = this._fetch(key).then(data => {
                    if (isArray(data)) { // continuous value
                        this.key2data[key] = data;
                    } else {
                        if (data.index) {  // sparse
                            let values = new Float32Array(this.schema.shape[0]);
                            for (let i = 0, n = data.index.length; i < n; i++) {
                                values[data.index[i]] = data.value[i];
                            }
                            this.key2data[key] = values;
                        } else {
                            this.key2data[key] = data; // object for coordinates
                        }
                    }

                });
                promises.push(p);
            }
        });
        return new Promise(resolve => {
            Promise.all(promises).then(() => resolve());
        });


    }

    getSelectedIdsPromise(q) {
        const dataFilter = q.filter;
        const {basis, X, obs} = splitDataFilter(dataFilter);
        let keys = [];
        basis.forEach(embedding => {
            keys.push(embedding.name);
        });
        keys.push('index');

        keys = keys.concat(X).concat(obs);
        return new Promise(resolve => {
            this.fetchData(keys).then(() => {
                const indices = Array.from(getPassingFilterIndices(this.key2data, dataFilter));
                let idVector = this.getVector('index', indices);
                let ids = [];
                for (let i = 0, n = idVector.size(); i < n; i++) {
                    ids.push(idVector.get(i));
                }
                resolve({ids: ids});
            });
        });
    }

    getDataPromise(q, cachedData) {
        let dimensions = [];
        let measures = [];
        let queryKeys = ['stats', 'groupedStats', 'embedding', 'selection', 'values'];
        const results = {};
        queryKeys.forEach(key => {
            if (key in q) {
                let obj = q[key];
                if (!isArray(obj)) {
                    obj = [obj];
                }
                obj.forEach(value => {
                    if (value.dimensions) {
                        dimensions = dimensions.concat(value.dimensions);
                    }
                    if (value.measures) {
                        measures = measures.concat(value.measures);
                    }
                });
            }
        });

        const typeToMeasures = getTypeToMeasures(measures);
        let basisKeys = new Set();

        if (q.selection) { // get any embeddings
            const dataFilter = q.selection.filter;
            const {basis, X, obs} = splitDataFilter(dataFilter);

            dimensions = dimensions.concat(obs);
            measures = measures.concat(X);
            const embeddings = q.selection.embeddings || [];
            let mappedEmbeddings = [];
            embeddings.forEach(embedding => {
                let basis = getBasis(embedding.basis, embedding.nbins, embedding.agg,
                    embedding.ndim || 2, embedding.precomputed);
                basisKeys.add(basis.name);
                mappedEmbeddings.push(basis);
            });
            q.selection.embeddings = mappedEmbeddings;
            basis.forEach(embedding => {
                basisKeys.add(embedding.name);
            });

        }
        if (q.embedding) {
            q.embedding.forEach(embedding => {
                let basis = getBasis(embedding.basis, embedding.nbins, embedding.agg,
                    embedding.ndim || 2, embedding.precomputed);
                basisKeys.add(basis.name);
                embedding.basis = basis;
            });
        }

        return new Promise(resolve => {

            this.fetchData(dimensions.concat(typeToMeasures.obs).concat(typeToMeasures.X).concat(Array.from(basisKeys))).then(() => {

                if (q.embedding) {
                    results.embeddings = [];
                    q.embedding.forEach(embedding => {
                        let coordinates = this.getVector(embedding.basis.name).asArray();
                        results.embeddings.push({name: embedding.basis.full_name, coordinates: coordinates});
                    });
                }
                if (q.values) {
                    let dimensions = q.values.dimensions || [];
                    let measures = q.values.measures || [];
                    const typeToMeasures = getTypeToMeasures(measures);
                    let values = {};
                    dimensions.concat(typeToMeasures.obs).concat(typeToMeasures.X).forEach(key => {
                        if (key === '__count') {
                            values[key] = new Int8Array(this.schema.shape[0]);
                            values[key].fill(1);
                        } else {
                            values[key] = this.getVector(key).asArray();
                        }
                    });
                    results.values = values;
                }
                cacheValues(results, cachedData);
                computeDerivedStats(results, q, cachedData);
                resolve(results);
            });
        });
    }

    getSchemaPromise() {
        if (this.schema != null) {
            return Promise.resolve(this.schema);
        }
        const url = this.url;
        const _this = this;
        if (this.format === 'jsonl') {
            return new Promise((resolve, reject) => {
                fetch(url + '.idx.json').then(r => r.json()).then(result => {
                    _this.key2bytes = result.index;
                }).then(() => {
                    fetch(url, _this.getByteRange('schema')).then(response => {
                        return response.json();
                    }).then(result => {
                        _this.schema = result["schema"];
                        resolve();
                    });
                });
            });
        } else {
            return new Promise((resolve, reject) => {
                fetch(url).then(r => r.json()).then(result => {
                    _this.schema = result;
                    resolve(result);
                });
            });
        }

    }

    getVector(key, indices = null) {
        let array = this.key2data[key];
        let v = new Vector(key, array);
        if (indices != null) {
            v = new SlicedVector(v, indices);
        }
        return v;
    }

    getFileUrl(file) {
        return this.baseUrl + file;
    }

    getJob(id, returnResults) {
        return fetch(this.baseUrl + 'uns/' + id + '.json').then(r => r.json());
    }

    getJobs() {
        return [];
    }

    getVectors(keys, indices = null) {
        let result = [];
        keys.forEach(key => {
            let v = this.getVector(key, indices);
            result.push(v);
        });
        return result;
    }


}




