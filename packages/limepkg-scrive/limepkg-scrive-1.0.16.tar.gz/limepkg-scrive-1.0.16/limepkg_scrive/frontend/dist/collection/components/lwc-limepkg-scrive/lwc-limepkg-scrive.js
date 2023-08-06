var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { h } from "@stencil/core";
import { Configs, CurrentLimeobject } from '@limetech/lime-web-components-decorators';
export class Test {
    constructor() {
        this.document = {};
        this.config = {};
        this.includePerson = false;
        this.allowedExtensions = Object.freeze(["PDF", "DOC", "DOCX"]);
    }
    goToScrive(id) {
        const host = this.config.limepkg_scrive.scriveHost;
        window.open(`${host}/public/?limeDocId=${id}${this.includePerson ? "&usePerson=true" : ""}`);
    }
    files() {
        var _a;
        const fileMap = ((_a = this.document) === null || _a === void 0 ? void 0 : _a._files) || {};
        const fileIds = Object.keys(fileMap);
        return fileIds.map(id => fileMap[id]);
    }
    isSignable(file) {
        return this.allowedExtensions.includes((file.extension || "").toUpperCase());
    }
    render() {
        if (this.context.limetype !== 'document') {
            return;
        }
        const signableFiles = this.files().filter(this.isSignable, this);
        const noSignableFiles = signableFiles.length === 0;
        const tooManySignableFiles = signableFiles.length > 1;
        if (noSignableFiles || tooManySignableFiles) {
            return;
        }
        return (h("div", null,
            h("limel-collapsible-section", { header: "Sign with Scrive" },
                h("limel-button", { label: `Design Contract`, outlined: true, onClick: () => this.goToScrive(this.context.id) }),
                h("limel-checkbox", { label: "Add associated person as signing party", id: "fab", checked: this.includePerson, required: false, onChange: () => this.includePerson = !this.includePerson }))));
    }
    static get is() { return "lwc-limepkg-scrive"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["lwc-limepkg-scrive.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["lwc-limepkg-scrive.css"]
    }; }
    static get properties() { return {
        "platform": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentPlatform",
                "resolved": "LimeWebComponentPlatform",
                "references": {
                    "LimeWebComponentPlatform": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "Reference to the platform"
            }
        },
        "context": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentContext",
                "resolved": "LimeWebComponentContext",
                "references": {
                    "LimeWebComponentContext": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "The context this component belongs to"
            }
        }
    }; }
    static get states() { return {
        "document": {},
        "config": {},
        "includePerson": {}
    }; }
    static get elementRef() { return "element"; }
}
__decorate([
    CurrentLimeobject()
], Test.prototype, "document", void 0);
__decorate([
    Configs({})
], Test.prototype, "config", void 0);
