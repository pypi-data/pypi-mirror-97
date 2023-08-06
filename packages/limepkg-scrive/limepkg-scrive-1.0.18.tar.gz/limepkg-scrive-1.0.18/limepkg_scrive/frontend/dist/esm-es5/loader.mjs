import { a as patchEsm, b as bootstrapLazy } from './core-8fd44f54.js';
var defineCustomElements = function (win, options) {
    return patchEsm().then(function () {
        bootstrapLazy([["lwc-limepkg-scrive", [[1, "lwc-limepkg-scrive", { "platform": [16], "context": [16], "document": [32], "session": [32], "config": [32], "includePerson": [32] }]]], ["lwc-limepkg-scrive-loader", [[1, "lwc-limepkg-scrive-loader", { "platform": [16], "context": [16] }]]]], options);
    });
};
export { defineCustomElements };
