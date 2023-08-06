import {
    LimeWebComponent,
    LimeWebComponentContext,
    LimeWebComponentPlatform,
    NotificationService,
    PlatformServiceName,
    LimeobjectsStateService
} from '@limetech/lime-web-components-interfaces';
import { Component, Element, h, Prop, State} from '@stencil/core';
import { Configs, CurrentLimeobject, Limeobjects} from '@limetech/lime-web-components-decorators';
import { ListItem, ListSeparator, ValidationStatus, Tab} from '@limetech/lime-elements';

type File = {
    extension: string,
    filename: string,
    size: number;
}

@Component({
    tag: 'lwc-limepkg-scrive',
    shadow: true,
    styleUrl: 'lwc-limepkg-scrive.scss',
})
export class Test implements LimeWebComponent {

    @CurrentLimeobject()
    @State()
    private document : any = {}

    @Prop()
    public platform: LimeWebComponentPlatform;

    @Configs({})
    @State()
    private config : any = {}

    @Prop()
    public context: LimeWebComponentContext;

    @Element()
    public element: HTMLElement;

    @State()
    public includePerson = false;


    private goToScrive(id) {
        const host = this.config.limepkg_scrive.scriveHost;
        window.open(`${host}/public/?limeDocId=${id}${ this.includePerson ? "&usePerson=true" : ""}`);
    }
    
    
    private files(): File[] {
        const fileMap = this.document?._files || {};
        const fileIds = Object.keys(fileMap);
        return fileIds.map(id => fileMap[id]);
    }
    
    private allowedExtensions = Object.freeze(["PDF", "DOC", "DOCX"]);
    private isSignable(file: File): boolean {
        return this.allowedExtensions.includes((file.extension || "").toUpperCase())
    }

    public render() {
        if (this.context.limetype !== 'document') {
            return;
        }

        const signableFiles = this.files().filter(this.isSignable, this);
        const noSignableFiles = signableFiles.length === 0;
        const tooManySignableFiles = signableFiles.length > 1
        if(noSignableFiles || tooManySignableFiles) {
            return;
        }

        return (
            <div>
                <limel-collapsible-section header="Sign with Scrive">
                    <limel-button
                        label={`Design Contract`}
                        outlined={true}
                        onClick={() =>
                            this.goToScrive(this.context.id)
                        }
                    />
                    <limel-checkbox
                        label="Add associated person as signing party"
                        id="fab"
                        checked={this.includePerson}
                        required={false}
                        onChange={() => this.includePerson = !this.includePerson}
                    />
                </limel-collapsible-section>
            </div>
        );
    }
}
