import { Component, h, Prop, State, Event } from '@stencil/core';
import { fetchVideos } from '../../services';
import { EnumViews } from '../../models/EnumViews';
export class LayoutVideoLibrary {
    constructor() {
        this.videos = [];
        this.isLoadingVideos = false;
        this.handelClose = this.handelClose.bind(this);
    }
    componentWillLoad() {
        this.loadVideos();
    }
    render() {
        return [
            h("div", { class: "video-library-container" },
                h("h3", null, "Select a video"),
                h("p", null, "It will be present for the recipient when they open the document."),
                this.isLoadingVideos && h("ga-loader", null),
                h("ul", { class: "video-list" }, this.videos.map(video => {
                    return h("video-thumb", { video: video });
                }))),
        ];
    }
    async loadVideos() {
        this.isLoadingVideos = true;
        const { videos } = await fetchVideos(this.platform, this.session);
        this.videos = videos.map((video) => {
            return {
                thumb_url: video.thumb_url,
                video_id: video.video_id,
                video_title: video.video_title,
                video_type: video.video_type,
                video_url: video.video_url,
            };
        });
        this.isLoadingVideos = false;
    }
    handelClose() {
        this.changeView.emit(EnumViews.sendDocument);
    }
    static get is() { return "layout-video-library"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["layout-video-library.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["layout-video-library.css"]
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
        "session": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "ISession",
                "resolved": "ISession",
                "references": {
                    "ISession": {
                        "location": "import",
                        "path": "../../types/Session"
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
        "videos": {},
        "isLoadingVideos": {}
    }; }
    static get events() { return [{
            "method": "changeView",
            "name": "changeView",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "any",
                "resolved": "any",
                "references": {}
            }
        }]; }
}
