import { Component, h, Prop, State, Listen, Event } from '@stencil/core';
import { PlatformServiceName, } from '@limetech/lime-web-components-interfaces';
export class LayoutSelectRecipient {
    constructor() {
        this.selectedRecipientList = [];
        this.includeCoworkers = false;
        this.recipientList = [];
        this.selectRecipientHandler = this.selectRecipientHandler.bind(this);
        this.isAdded = this.isAdded.bind(this);
        this.onSearch = this.onSearch.bind(this);
        this.toggleIncludeCoworkers = this.toggleIncludeCoworkers.bind(this);
        this.fetchRecipients = this.fetchRecipients.bind(this);
    }
    componentWillLoad() {
        this.selectedRecipientList = this.document.recipients;
    }
    render() {
        return [
            h("div", { class: "select-recipient-container" },
                h("div", { class: "recipient-container" },
                    h("h3", null, "Search Recipient"),
                    h("div", { class: "recipient-toolbar" },
                        h("limel-input-field", { label: "Search recipient", value: this.searchTerm, onChange: this.onSearch }),
                        h("limel-switch", { label: "Include coworkers", value: this.includeCoworkers, onChange: this.toggleIncludeCoworkers })),
                    h("ul", { class: "recipient-list" }, this.recipientList.map(recipient => {
                        if (!this.isAdded(recipient.lime_id)) {
                            return (h("recipient-item", { recipient: recipient, showAdd: true, onClick: () => {
                                    this.selectRecipientHandler(recipient);
                                } }));
                        }
                    }))),
                h("div", { class: "selected-recipient-container" },
                    h("h3", null, "Added recipients"),
                    h("selected-recipient-list", { recipients: this.selectedRecipientList, document: this.document }))),
        ];
    }
    selectRecipientHandler(recipient) {
        if (!!recipient.mobile || !!recipient.email) {
            this.selectedRecipientList = [
                ...this.selectedRecipientList,
                recipient,
            ];
            this.updateDocumentRecipient.emit(this
                .selectedRecipientList);
        }
        else {
            this.errorHandler.emit('A recipient needs to have a mobile number or an email address');
        }
    }
    removeRecipientHandler(recipient) {
        let rec = recipient.detail;
        this.selectedRecipientList = this.selectedRecipientList.filter(recipientData => {
            return recipientData.lime_id != rec.lime_id;
        });
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    }
    changeRecipientRoleHandler(recipient) {
        const recipientData = recipient.detail;
        const index = this.selectedRecipientList.findIndex(rec => rec.lime_id === recipientData.lime_id);
        this.selectedRecipientList[index] = recipientData;
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    }
    isAdded(recipientId) {
        return !!this.selectedRecipientList.find(recipient => recipient.lime_id === recipientId);
    }
    toggleIncludeCoworkers() {
        this.includeCoworkers = !this.includeCoworkers;
        this.fetchRecipients();
    }
    async onSearch(event) {
        this.searchTerm = event.detail;
        this.fetchRecipients();
    }
    async fetchRecipients() {
        const options = {
            params: {
                search: this.searchTerm,
                limit: '10',
                offset: '0',
            },
        };
        try {
            const persons = await this.fetchPersons(options);
            const coworkers = await this.fetchCoworkers(options, this.includeCoworkers);
            this.recipientList = [...persons, ...coworkers];
        }
        catch (e) {
            this.errorHandler.emit('Something went wrong while communicating with the server...');
        }
    }
    async fetchPersons(options) {
        const persons = await this.platform
            .get(PlatformServiceName.Http)
            .get('getaccept/persons', options);
        return persons.map(person => ({
            email: person.email,
            name: person.name,
            mobile: person.mobilephone || person.phone,
            limetype: 'person',
            lime_id: person.id,
            company: person.company,
        }));
    }
    async fetchCoworkers(options, includeCoworkers) {
        if (!includeCoworkers) {
            return [];
        }
        const coworkers = await this.platform
            .get(PlatformServiceName.Http)
            .get('getaccept/coworkers', options);
        return coworkers.map(coworker => ({
            mobile: coworker.mobilephone || coworker.phone,
            name: coworker.name,
            email: coworker.email,
            limetype: 'coworker',
            lime_id: coworker.id,
            company: coworker.company,
        }));
    }
    static get is() { return "layout-select-recipient"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["layout-select-recipient.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["layout-select-recipient.css"]
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
                "text": ""
            }
        },
        "document": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IDocument",
                "resolved": "IDocument",
                "references": {
                    "IDocument": {
                        "location": "import",
                        "path": "../../types/Document"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        }
    }; }
    static get states() { return {
        "searchTerm": {},
        "selectedRecipientList": {},
        "includeCoworkers": {},
        "recipientList": {}
    }; }
    static get events() { return [{
            "method": "updateDocumentRecipient",
            "name": "updateDocumentRecipient",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "IRecipient[]",
                "resolved": "IRecipient[]",
                "references": {
                    "IRecipient": {
                        "location": "import",
                        "path": "../../types/Recipient"
                    }
                }
            }
        }, {
            "method": "errorHandler",
            "name": "errorHandler",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "string",
                "resolved": "string",
                "references": {}
            }
        }]; }
    static get listeners() { return [{
            "name": "removeRecipient",
            "method": "removeRecipientHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "changeRecipientRole",
            "method": "changeRecipientRoleHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }]; }
}
