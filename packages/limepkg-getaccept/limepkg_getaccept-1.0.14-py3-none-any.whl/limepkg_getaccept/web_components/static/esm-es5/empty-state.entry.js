import { r as registerInstance, h } from './index-570406ba.js';
var emptyStateCss = ".empty-state{margin-top:1.5rem;font-style:italic;text-align:center;opacity:0.8}.empty-state limel-icon{width:3rem;height:3rem}";
var EmptyState = /** @class */ (function () {
    function EmptyState(hostRef) {
        registerInstance(this, hostRef);
        this.icon = 'nothing_found';
    }
    EmptyState.prototype.render = function () {
        return (h("div", { class: "empty-state" }, h("limel-icon", { name: this.icon }), h("p", null, this.text)));
    };
    return EmptyState;
}());
EmptyState.style = emptyStateCss;
export { EmptyState as empty_state };
