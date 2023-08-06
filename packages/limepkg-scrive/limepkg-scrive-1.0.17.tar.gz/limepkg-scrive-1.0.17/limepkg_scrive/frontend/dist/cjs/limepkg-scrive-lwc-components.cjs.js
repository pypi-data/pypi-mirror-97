'use strict';

const core = require('./core-1b3ed83d.js');

core.patchBrowser().then(options => {
  return core.bootstrapLazy([["lwc-limepkg-scrive.cjs",[[1,"lwc-limepkg-scrive",{"platform":[16],"context":[16],"document":[32],"config":[32],"includePerson":[32]}]]],["lwc-limepkg-scrive-loader.cjs",[[1,"lwc-limepkg-scrive-loader",{"platform":[16],"context":[16]}]]]], options);
});
