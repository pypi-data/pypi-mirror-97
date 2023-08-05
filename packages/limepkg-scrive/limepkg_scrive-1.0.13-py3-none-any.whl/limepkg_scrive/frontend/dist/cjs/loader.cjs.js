'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const core = require('./core-12852af1.js');

const defineCustomElements = (win, options) => {
  return core.patchEsm().then(() => {
    core.bootstrapLazy([["lwc-limepkg-scrive-loader.cjs",[[1,"lwc-limepkg-scrive-loader",{"platform":[16],"context":[16]}]]],["lwc-limepkg-scrive-test.cjs",[[1,"lwc-limepkg-scrive-test",{"platform":[16],"context":[16],"document":[32],"config":[32],"includePerson":[32]}]]]], options);
  });
};

exports.defineCustomElements = defineCustomElements;
