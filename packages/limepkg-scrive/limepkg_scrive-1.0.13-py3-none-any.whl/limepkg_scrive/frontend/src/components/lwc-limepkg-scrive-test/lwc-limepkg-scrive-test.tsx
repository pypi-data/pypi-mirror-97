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
    tag: 'lwc-limepkg-scrive-test',
    shadow: true,
    styleUrl: 'lwc-limepkg-scrive-test.scss',
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


        const files = this.files();
        const signableFiles = files.filter(this.isSignable, this);
        const noSignableFiles = signableFiles.length === 0;
        const tooManySignableFiles = signableFiles.length > 1
        const signingDisabled = noSignableFiles || tooManySignableFiles;
        const items = files.map(f => {
            if(this.isSignable(f)) {
                return { text: `${f.filename} is signable.`}
            }
            return { text: `${f.filename} is not signable.`}
        });
        return (
            <div>
                <limel-collapsible-section header="Sign with Scrive">
                    <limel-button
                        label={`Design Contract`}
                        outlined={true}
                        disabled={signingDisabled}
                        onClick={() =>
                            this.goToScrive(this.context.id)
                        }
                    />
                    <limel-checkbox
                        label="Add associated person as signing party"
                        id="fab"
                        checked={this.includePerson}
                        required={false}
                        disabled={signingDisabled}
                        onChange={() => this.includePerson = !this.includePerson}
                    />
                    {noSignableFiles && (
                        <limel-dialog heading="No Signable Files" open={true}>
                            There are no signable files.
                            <limel-list items={items}></limel-list>
                            Please keep in mind that only certain types ({this.allowedExtensions.join(", ")}) of these types of files are signable.
                        </limel-dialog>
                    )}
                    {tooManySignableFiles && (
                        <limel-dialog heading="Too Many Signable Files" open={true}>
                            Only one file is signable at a time.
                            <limel-list items={items}></limel-list>
                        </limel-dialog>
                    )}
                </limel-collapsible-section>
            </div>
        );
    }
}
