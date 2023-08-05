import { a as patchEsm, b as bootstrapLazy } from './core-2d5e9821.js';

const defineCustomElements = (win, options) => {
  return patchEsm().then(() => {
    bootstrapLazy([["lwc-limepkg-scrive-loader",[[1,"lwc-limepkg-scrive-loader",{"platform":[16],"context":[16]}]]],["lwc-limepkg-scrive-test",[[1,"lwc-limepkg-scrive-test",{"platform":[16],"context":[16],"document":[32],"config":[32],"includePerson":[32]}]]]], options);
  });
};

export { defineCustomElements };
