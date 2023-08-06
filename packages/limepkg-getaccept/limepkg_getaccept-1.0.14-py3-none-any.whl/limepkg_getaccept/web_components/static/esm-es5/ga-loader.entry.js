import { r as registerInstance, h } from './index-570406ba.js';
var gaLoaderCss = "limel-spinner{margin:1rem 0;color:#f49132}";
var GALoader = /** @class */ (function () {
    function GALoader(hostRef) {
        registerInstance(this, hostRef);
    }
    GALoader.prototype.render = function () {
        return (h("limel-flex-container", { justify: "center" }, h("limel-spinner", null)));
    };
    return GALoader;
}());
GALoader.style = gaLoaderCss;
export { GALoader as ga_loader };
