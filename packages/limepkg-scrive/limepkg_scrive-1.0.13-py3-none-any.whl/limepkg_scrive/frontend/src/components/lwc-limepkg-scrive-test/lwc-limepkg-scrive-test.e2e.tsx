import { newE2EPage } from '@stencil/core/testing';

describe('lwc-limepkg-scrive-test', () => {
    let page;
    beforeEach(async () => {
        page = await newE2EPage();
    });

    describe('render', () => {
        let button;
        beforeEach(async () => {
            await page.setContent(`
                <lwc-limepkg-scrive-test></lwc-limepkg-scrive-test>
            `);
            await page.find('lwc-limepkg-scrive-test');

            // `>>>` means that `limel-button` is inside the
            // shadow-DOM of `lwc-limepkg-scrive-test`
            button = await page.find(`
                lwc-limepkg-scrive-test >>> limel-button
            `);
        });
        it('displays the correct label', () => {
            expect(button).toEqualAttribute('label', 'Hello World!');
        });
    });
});
