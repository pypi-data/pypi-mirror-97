import { LimeWebComponent, LimeWebComponentContext, LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
export declare class Test implements LimeWebComponent {
    private document;
    private session;
    platform: LimeWebComponentPlatform;
    private config;
    context: LimeWebComponentContext;
    element: HTMLElement;
    includePerson: boolean;
    private goToScrive;
    private files;
    private allowedExtensions;
    private isSignable;
    render(): any;
}
