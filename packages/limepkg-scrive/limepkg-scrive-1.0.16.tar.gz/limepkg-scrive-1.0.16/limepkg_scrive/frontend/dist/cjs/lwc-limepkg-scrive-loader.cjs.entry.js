'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const core = require('./core-1b3ed83d.js');

const Loader = class {
    constructor(hostRef) {
        core.registerInstance(this, hostRef);
    }
    componentWillLoad() {
        // tslint:disable-line:no-empty
    }
    componentDidUnload() {
        // tslint:disable-line:no-empty
    }
};

exports.lwc_limepkg_scrive_loader = Loader;
