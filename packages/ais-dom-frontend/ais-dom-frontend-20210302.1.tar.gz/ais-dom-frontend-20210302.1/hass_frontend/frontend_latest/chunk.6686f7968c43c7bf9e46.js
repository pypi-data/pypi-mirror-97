(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6447],{81545:(e,t,i)=>{"use strict";i(53918),i(42299);var r=i(15652);i(10983);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!s(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,p.elements)}),i),p=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(s(n)||s(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(s(n)){if(s(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}a(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,p.elements),c.runClassFinishers(h.F,p.finishers)}([(0,r.Mo)("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return r.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),r.oi)},36125:(e,t,i)=>{"use strict";i(59947);var r=i(15652);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!s(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function p(e,t,i){return(p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=m(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function m(e){return(m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const u=customElements.get("mwc-fab");!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,p.elements)}),i),p=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(s(n)||s(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(s(n)){if(s(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}a(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,p.elements),c.runClassFinishers(h.F,p.finishers)}([(0,r.Mo)("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){p(m(i.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),u)},81303:(e,t,i)=>{"use strict";i(8878);const r=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends r{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},13997:(e,t,i)=>{"use strict";i(53918),i(36051),i(81689);var r=i(55317),o=(i(53973),i(51095),i(54444),i(15652)),n=i(81471),a=i(49629),s=i(79865),l=i(47181),c=i(87744),d=i(38346),h=i(69371),p=i(26765),m=i(54845),u=i(11654),f=i(27322);i(74535),i(81545),i(22098),i(31206),i(36125),i(81303),i(52039);const y=()=>Promise.all([i.e(2762),i.e(1063),i.e(1123),i.e(8048),i.e(9783),i.e(7757),i.e(9005),i.e(7797)]).then(i.bind(i,24841));function v(){v=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!w(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return E(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?E(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=x(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function g(e){var t,i=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function b(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function E(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function $(e,t,i){return($="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=P(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function P(e){return(P=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var o=v();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(k(n.descriptor)||k(o.descriptor)){if(w(n)||w(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(w(n)){if(w(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}b(n,o)}else t.push(n)}return t}(a.d.map(g)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("ha-media-player-browse")],(function(e,t){class v extends t{constructor(...t){super(...t),e(this)}}return{F:v,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"mediaContentId",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"mediaContentType",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"action",value:()=>"play"},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"dialog",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,attribute:"narrow",reflect:!0})],key:"_narrow",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,attribute:"scroll",reflect:!0})],key:"_scrolled",value:()=>!1},{kind:"field",decorators:[(0,o.sz)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,o.sz)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_mediaPlayerItems",value:()=>[]},{kind:"field",decorators:[(0,o.IO)(".header")],key:"_header",value:void 0},{kind:"field",decorators:[(0,o.IO)(".content")],key:"_content",value:void 0},{kind:"field",key:"_headerOffsetHeight",value:()=>0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"connectedCallback",value:function(){$(P(v.prototype),"connectedCallback",this).call(this),this.updateComplete.then((()=>this._attachObserver()))}},{kind:"method",key:"disconnectedCallback",value:function(){this._resizeObserver&&this._resizeObserver.disconnect()}},{kind:"method",key:"navigateBack",value:function(){this._mediaPlayerItems.pop();const e=this._mediaPlayerItems.pop();e&&this._navigate(e)}},{kind:"method",key:"render",value:function(){var e;if(this._loading)return o.dy`<ha-circular-progress active></ha-circular-progress>`;if(this._error&&!this._mediaPlayerItems.length){if(!this.dialog)return o.dy`
          <div class="container">
            ${this._renderError(this._error)}
          </div>
        `;this._closeDialogAction(),(0,p.Ys)(this,{title:this.hass.localize("ui.components.media-browser.media_browsing_error"),text:this._renderError(this._error)})}if(!this._mediaPlayerItems.length)return o.dy``;const t=this._mediaPlayerItems[this._mediaPlayerItems.length-1],i="media-source://media_source/galeria/."===t.media_content_id,l=this._mediaPlayerItems.length>1?this._mediaPlayerItems[this._mediaPlayerItems.length-2]:void 0,d=this.hass.localize(`ui.components.media-browser.class.${t.media_class}`),m=h.Fn[t.media_class],u=h.Fn[t.children_media_class];return o.dy`
      <div
        class="header ${(0,n.$)({"no-img":!t.thumbnail,"no-dialog":!this.dialog})}"
        @transitionend=${this._setHeaderHeight}
      >
        <div class="header-content">
          ${t.thumbnail?o.dy`
                <div
                  class="img"
                  style=${(0,s.V)({backgroundImage:t.thumbnail?`url(${t.thumbnail})`:"none"})}
                >
                  ${this._narrow&&(null==t?void 0:t.can_play)?o.dy`
                        <ha-fab
                          mini
                          .item=${t}
                          @click=${this._actionClicked}
                        >
                          <ha-svg-icon
                            slot="icon"
                            .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                            .path=${"play"===this.action?r._86:r.qX5}
                          ></ha-svg-icon>
                          ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                        </ha-fab>
                      `:""}
                </div>
              `:o.dy``}
          <div class="header-info">
            <div class="breadcrumb">
              ${l?o.dy`
                    <div class="previous-title" @click=${this.navigateBack}>
                      <ha-svg-icon .path=${r.J3k}></ha-svg-icon>
                      ${l.title}
                    </div>
                  `:""}
              <h1 class="title">${t.title}</h1>
              ${d?o.dy`
                    <h2 class="subtitle">
                      ${d}
                    </h2>
                  `:""}
            </div>
            ${!t.can_play||t.thumbnail&&this._narrow?"":o.dy`
                  <mwc-button
                    raised
                    .item=${t}
                    @click=${this._actionClicked}
                  >
                    <ha-svg-icon
                      .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                      .path=${"play"===this.action?r._86:r.qX5}
                    ></ha-svg-icon>
                    ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                  </mwc-button>
                `}
          </div>
        </div>
        ${this.dialog?o.dy`
              <mwc-icon-button
                aria-label=${this.hass.localize("ui.dialogs.generic.close")}
                @click=${this._closeDialogAction}
                class="header_button"
                dir=${(0,c.Zu)(this.hass)}
              >
                <ha-svg-icon .path=${r.r5M}></ha-svg-icon>
              </mwc-icon-button>
            `:""}
      </div>
      <div class="content" @scroll=${this._scroll} @touchmove=${this._scroll}>
        ${this._error?o.dy`
              <div class="container">
                ${this._renderError(this._error)}
              </div>
            `:(null===(e=t.children)||void 0===e?void 0:e.length)?"grid"===u.layout?o.dy`
                <div
                  class="children ${(0,n.$)({portrait:"portrait"===u.thumbnail_ratio})}"
                >
                  ${t.children.map((e=>o.dy`
                      <div
                        class="child"
                        .item=${e}
                        @click=${this._childClicked}
                      >
                        <div class="ha-card-parent">
                          <ha-card
                            outlined
                            style=${(0,s.V)({backgroundImage:e.thumbnail?`url(${e.thumbnail})`:"none"})}
                          >
                            ${e.thumbnail?"":o.dy`
                                  <ha-svg-icon
                                    class="folder"
                                    .path=${h.Fn["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
                                  ></ha-svg-icon>
                                `}
                          </ha-card>
                          ${e.can_play?o.dy`
                                <mwc-icon-button
                                  class="play ${(0,n.$)({can_expand:e.can_expand})}"
                                  .item=${e}
                                  .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                  @click=${this._actionClicked}
                                >
                                  <ha-svg-icon
                                    .path=${"play"===this.action?r._86:r.qX5}
                                  ></ha-svg-icon>
                                </mwc-icon-button>
                              `:""}
                        </div>
                        <!-- AIS add info button for admins only aisGallery-->
                        ${this._getAisImageButtons(i,e,u.layout)}
                      </div>
                    `))}
                </div>
              `:o.dy`
                <mwc-list>
                  ${t.children.map((e=>o.dy`
                      <mwc-list-item
                        @click=${this._childClicked}
                        .item=${e}
                        graphic="avatar"
                        hasMeta
                        dir=${(0,c.Zu)(this.hass)}
                      >
                        <div
                          class="graphic"
                          style=${(0,a.o)(m.show_list_images&&e.thumbnail?`background-image: url(${e.thumbnail})`:void 0)}
                          slot="graphic"
                        >
                          <mwc-icon-button
                            class="play ${(0,n.$)({show:!m.show_list_images||!e.thumbnail})}"
                            .item=${e}
                            .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                            @click=${this._actionClicked}
                          >
                            <ha-svg-icon
                              .path=${"play"===this.action?r._86:r.qX5}
                            ></ha-svg-icon>
                          </mwc-icon-button>
                        </div>
                        <span class="title">${e.title}</span>
                        <!-- AIS add info button for admins only aisGallery-->
                        ${this._getAisImageButtons(i,e,u.layout)}
                      </mwc-list-item>
                      <li divider role="separator"></li>
                    `))}
                </mwc-list>
              `:o.dy`
              <div class="container">
                ${this.hass.localize("ui.components.media-browser.no_items")}
                <br />
                ${i?o.dy`<br />${this.hass.localize("ui.components.media-browser.learn_adding_local_media","documentation",o.dy`<a
                          href="https://www.ai-speaker.com/docs/ais_app_integration_gallery"
                          target="_blank"
                          rel="noreferrer"
                          >${this.hass.localize("ui.components.media-browser.documentation")}</a
                        >`)}
                      <br />
                      ${this.hass.localize("ui.components.media-browser.local_media_files")}`:""}
              </div>
            `}
        ${this._getAisImageFabButton(i)}
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(){this._measureCard(),this._attachObserver()}},{kind:"method",key:"updated",value:function(e){$(P(v.prototype),"updated",this).call(this,e),e.has("_mediaPlayerItems")&&this._mediaPlayerItems.length&&this._setHeaderHeight(),void 0!==e.get("_scrolled")&&this._mediaPlayerItems.length&&this._animateHeaderHeight(),(e.has("entityId")||e.has("mediaContentId")||e.has("mediaContentType")||e.has("action"))&&(e.has("entityId")&&(this._error=void 0,this._mediaPlayerItems=[]),this._fetchData(this.mediaContentId,this.mediaContentType).then((e=>{e&&(this._mediaPlayerItems=[e])})).catch((e=>{this._error=e})))}},{kind:"method",key:"_setHeaderHeight",value:async function(){await this.updateComplete;const e=this._header,t=this._content;e&&t&&(this._headerOffsetHeight=e.offsetHeight,t.style.marginTop=`${this._headerOffsetHeight}px`,t.style.maxHeight=`calc(var(--media-browser-max-height, 100%) - ${this._headerOffsetHeight}px)`)}},{kind:"method",key:"_animateHeaderHeight",value:function(){let e;const t=i=>{void 0===e&&(e=i);const r=i-e;this._setHeaderHeight(),r<400&&requestAnimationFrame(t)};requestAnimationFrame(t)}},{kind:"method",key:"_actionClicked",value:function(e){e.stopPropagation();const t=e.currentTarget.item;this._runAction(t)}},{kind:"method",key:"_getAisImageFabButton",value:function(e){return e?o.dy` <mwc-fab
        slot="fab"
        title="Dodaj"
        @click=${this._addImage}
        class="addImageFab"
      >
        <ha-svg-icon slot="icon" path=${r.qX5}></ha-svg-icon>
      </mwc-fab>`:o.dy``}},{kind:"method",key:"_getAisImageButtons",value:function(e,t,i){const n="grid"===i?"":"Line";return this.hass.user.is_admin&&e?o.dy` <div class="aisButtons${n}">
        <mwc-icon-button
          class="aisButton${n} aisInfoButton"
          .item=${t}
          @click=${this._actionClickedInfo}
        >
          <ha-svg-icon path=${r.geb}></ha-svg-icon>
        </mwc-icon-button>
        <mwc-icon-button
          class="aisButton${n} aisEditButton"
          .item=${t}
          @click=${this._actionClickedEdit}
        >
          <ha-svg-icon path=${r.LgD}></ha-svg-icon>
        </mwc-icon-button>
        <mwc-icon-button
          class="aisButton${n} aisDeleteButton"
          .item=${t}
          @click=${this._actionClickedDelete}
        >
          <ha-svg-icon path=${r.x9U}></ha-svg-icon>
        </mwc-icon-button>
      </div>`:t.can_play&&this.hass.user.is_admin&&!e?o.dy` <div class="aisButtons${n}">
        <mwc-icon-button
          class="aisButton${n} aisInfoButton"
          .item=${t}
          @click=${this._actionClickedInfo}
        >
          <ha-svg-icon path=${r.geb}></ha-svg-icon>
        </mwc-icon-button>
      </div>`:e?o.dy``:o.dy` <div class="title">
          ${t.title}
          <paper-tooltip fitToVisibleBounds position="top" offset="4"
            >${t.title}</paper-tooltip
          >
        </div>
        <div class="type">
          ${this.hass.localize(`ui.components.media-browser.content-type.${t.media_content_type}`)}
        </div>`}},{kind:"method",key:"_actionClickedInfo",value:async function(e){e.stopPropagation();const t=e.currentTarget.item,r=await this.hass.callWS({type:"media_source/resolve_media",media_content_id:t.media_content_id});var o,n;o=this,n={sourceUrl:r.url,sourceType:r.mime_type,sourceThumbnail:t.thumbnail,title:t.title},(0,l.B)(o,"show-dialog",{dialogTag:"hui-dialog-web-browser-ais-play-media",dialogImport:()=>Promise.all([i.e(2762),i.e(1063),i.e(319),i.e(9783),i.e(9239)]).then(i.bind(i,112)),dialogParams:n})}},{kind:"method",key:"_actionClickedEdit",value:async function(e){e.stopPropagation();const t=e.currentTarget.item,r=await this.hass.callWS({type:"media_source/resolve_media",media_content_id:t.media_content_id});(0,l.B)(this,"show-dialog",{dialogTag:"hui-dialog-web-browser-ais-edit-image",dialogImport:()=>Promise.all([i.e(2762),i.e(1063),i.e(319),i.e(9783),i.e(6668)]).then(i.bind(i,85494)),dialogParams:{sourceUrl:r.url,sourceType:r.mime_type,title:t.title}})}},{kind:"method",key:"_actionClickedDelete",value:async function(e){e.stopPropagation();const t=e.currentTarget.item;if(await(0,p.g7)(this,{title:t.title,text:"Jesteś pewny, że chcesz usunąć ten plik?",confirmText:"TAK",dismissText:"NIE"})){const e=await this.hass.callWS({type:"media_source/resolve_media",media_content_id:t.media_content_id});await this.hass.callService("ais_files","remove_file",{path:e.url}),this._navigate(this._mediaPlayerItems[this._mediaPlayerItems.length-1])}}},{kind:"method",key:"_runAction",value:function(e){(0,l.B)(this,"media-picked",{item:e})}},{kind:"method",key:"_childClicked",value:async function(e){const t=e.currentTarget.item;t&&(t.can_expand?this._navigate(t):this._runAction(t))}},{kind:"method",key:"_navigate",value:async function(e){var t;let i;this._error=void 0;try{i=await this._fetchData(e.media_content_id,e.media_content_type)}catch(e){return(0,p.Ys)(this,{title:this.hass.localize("ui.components.media-browser.media_browsing_error"),text:this._renderError(e)}),void(this._loading=!1)}null===(t=this._content)||void 0===t||t.scrollTo(0,0),this._scrolled=!1,this._mediaPlayerItems=[...this._mediaPlayerItems,i]}},{kind:"method",key:"_fetchData",value:async function(e,t){let i;this._loading=!0;try{i=this.entityId!==h.N8?await(0,h.zz)(this.hass,this.entityId,e,t):await(0,h.b)(this.hass,e,t)}finally{this._loading=!1}return i}},{kind:"method",key:"_measureCard",value:function(){this._narrow=(this.dialog?window.innerWidth:this.offsetWidth)<450}},{kind:"method",decorators:[(0,o.hO)({passive:!0})],key:"_scroll",value:function(e){const t=e.currentTarget;!this._scrolled&&t.scrollTop>this._headerOffsetHeight?this._scrolled=!0:this._scrolled&&t.scrollTop<this._headerOffsetHeight&&(this._scrolled=!1)}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(await(0,m.P)(),this._resizeObserver=new ResizeObserver((0,d.D)((()=>this._measureCard()),250,!1))),this._resizeObserver.observe(this)}},{kind:"method",key:"_closeDialogAction",value:function(){(0,l.B)(this,"close-dialog")}},{kind:"method",key:"_renderError",value:function(e){return"Media directory does not exist."===e.message?o.dy`
        <h2>
          ${this.hass.localize("ui.components.media-browser.no_local_media_found")}
        </h2>
        <p>
          ${this.hass.localize("ui.components.media-browser.no_media_folder")}
          <br />
          ${this.hass.localize("ui.components.media-browser.setup_local_help","documentation",o.dy`<a
              href="${(0,f.R)(this.hass,"/more-info/local-media/setup-media")}"
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.components.media-browser.documentation")}</a
            >`)}
          <br />
          ${this.hass.localize("ui.components.media-browser.local_media_files")}
        </p>
      `:o.dy`<span class="error">${e.message}</span>`}},{kind:"method",key:"_addImage",value:function(){const e=this._mediaPlayerItems[this._mediaPlayerItems.length-1];((e,t)=>{(0,l.B)(e,"show-dialog",{dialogTag:"ha-dialog-aisgalery",dialogImport:y,dialogParams:t})})(this,{jsCallback:()=>{this._navigate(e)}})}},{kind:"get",static:!0,key:"styles",value:function(){return[u.Qx,o.iv`
        :host {
          display: flex;
          flex-direction: column;
          position: relative;
        }

        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin: 40px;
        }

        .container {
          padding: 16px;
        }

        .content {
          overflow-y: auto;
          padding-bottom: 20px;
          box-sizing: border-box;
        }

        .header {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid var(--divider-color);
          background-color: var(--card-background-color);
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          z-index: 5;
          padding: 20px 24px 10px;
        }

        .header_button {
          position: relative;
          right: -8px;
        }

        .header-content {
          display: flex;
          flex-wrap: wrap;
          flex-grow: 1;
          align-items: flex-start;
        }

        .header-content .img {
          height: 200px;
          width: 200px;
          margin-right: 16px;
          background-size: cover;
          border-radius: 4px;
          transition: width 0.4s, height 0.4s;
        }

        .header-info {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          align-self: stretch;
          min-width: 0;
          flex: 1;
        }

        .header-info mwc-button {
          display: block;
          --mdc-theme-primary: var(--primary-color);
        }

        .breadcrumb {
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-grow: 1;
        }

        .breadcrumb .title {
          font-size: 32px;
          line-height: 1.2;
          font-weight: bold;
          margin: 0;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          padding-right: 8px;
        }

        .breadcrumb .previous-title {
          font-size: 14px;
          padding-bottom: 8px;
          color: var(--secondary-text-color);
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
          --mdc-icon-size: 14px;
        }

        .breadcrumb .subtitle {
          font-size: 16px;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 0;
          transition: height 0.5s, margin 0.5s;
        }

        /* ============= CHILDREN ============= */

        mwc-list {
          --mdc-list-vertical-padding: 0;
          --mdc-list-item-graphic-margin: 0;
          --mdc-theme-text-icon-on-background: var(--secondary-text-color);
          margin-top: 10px;
        }

        mwc-list li:last-child {
          display: none;
        }

        mwc-list li[divider] {
          border-bottom-color: var(--divider-color);
        }

        .children {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.1fr)
          );
          grid-gap: 16px;
          padding: 0px 24px;
          margin: 8px 0px;
        }

        :host([dialog]) .children {
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.33fr)
          );
        }

        .child {
          display: flex;
          flex-direction: column;
          cursor: pointer;
        }

        .ha-card-parent {
          position: relative;
          width: 100%;
        }

        .children ha-card {
          width: 100%;
          padding-bottom: 100%;
          position: relative;
          box-sizing: border-box;
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
          transition: padding-bottom 0.1s ease-out;
        }

        .portrait.children ha-card {
          padding-bottom: 150%;
        }

        .child .folder,
        .child .play {
          position: absolute;
        }

        .child .folder {
          color: var(--secondary-text-color);
          top: calc(50% - (var(--mdc-icon-size) / 2));
          left: calc(50% - (var(--mdc-icon-size) / 2));
          --mdc-icon-size: calc(var(--media-browse-item-size, 175px) * 0.4);
        }

        .child .play {
          transition: color 0.5s;
          border-radius: 50%;
          bottom: calc(50% - 35px);
          right: calc(50% - 35px);
          opacity: 0;
          transition: opacity 0.1s ease-out;
        }

        .child .play:not(.can_expand) {
          --mdc-icon-button-size: 70px;
          --mdc-icon-size: 48px;
        }

        .ha-card-parent:hover .play:not(.can_expand) {
          opacity: 1;
          color: var(--primary-color);
        }

        .child .play.can_expand {
          opacity: 1;
          bottom: -4px;
          right: 4px;
          z-index: 9999;
        }

        .child .play:hover {
          color: var(--primary-color);
        }

        .ha-card-parent:hover ha-card {
          opacity: 0.5;
        }

        .child .title {
          font-size: 16px;
          padding-top: 8px;
          padding-left: 2px;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          text-overflow: ellipsis;
        }

        .child .type {
          font-size: 12px;
          color: var(--secondary-text-color);
          padding-left: 2px;
        }

        mwc-list-item .graphic {
          background-size: cover;
        }

        mwc-list-item .graphic .play {
          opacity: 0;
          transition: all 0.5s;
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          border-radius: 50%;
          --mdc-icon-button-size: 40px;
        }

        mwc-list-item:hover .graphic .play {
          opacity: 1;
          color: var(--primary-color);
        }

        mwc-list-item .graphic .play.show {
          opacity: 1;
          background-color: transparent;
        }

        mwc-list-item .title {
          margin-left: 16px;
        }
        mwc-list-item[dir="rtl"] .title {
          margin-right: 16px;
          margin-left: 0;
        }

        /* ============= Narrow ============= */

        :host([narrow]) {
          padding: 0;
        }

        :host([narrow]) .breadcrumb .title {
          font-size: 24px;
        }

        :host([narrow]) .header {
          padding: 0;
        }

        :host([narrow]) .header.no-dialog {
          display: block;
        }

        :host([narrow]) .header_button {
          position: absolute;
          top: 14px;
          right: 8px;
        }

        :host([narrow]) .header-content {
          flex-direction: column;
          flex-wrap: nowrap;
        }

        :host([narrow]) .header-content .img {
          height: auto;
          width: 100%;
          margin-right: 0;
          padding-bottom: 50%;
          margin-bottom: 8px;
          position: relative;
          background-position: center;
          border-radius: 0;
          transition: width 0.4s, height 0.4s, padding-bottom 0.4s;
        }

        ha-fab {
          position: absolute;
          --mdc-theme-secondary: var(--primary-color);
          bottom: -20px;
          right: 20px;
        }

        :host([narrow]) .header-info mwc-button {
          margin-top: 16px;
          margin-bottom: 8px;
        }

        :host([narrow]) .header-info {
          padding: 20px 24px 10px;
        }

        :host([narrow]) .media-source {
          padding: 0 24px;
        }

        :host([narrow]) .children {
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        }

        /* ============= Scroll ============= */

        :host([scroll]) .breadcrumb .subtitle {
          height: 0;
          margin: 0;
        }

        :host([scroll]) .breadcrumb .title {
          -webkit-line-clamp: 1;
        }

        :host(:not([narrow])[scroll]) .header:not(.no-img) mwc-icon-button {
          align-self: center;
        }

        :host([scroll]) .header-info mwc-button,
        .no-img .header-info mwc-button {
          padding-right: 4px;
        }

        :host([scroll][narrow]) .no-img .header-info mwc-button {
          padding-right: 16px;
        }

        :host([scroll]) .header-info {
          flex-direction: row;
        }

        :host([scroll]) .header-info mwc-button {
          align-self: center;
          margin-top: 0;
          margin-bottom: 0;
        }

        :host([scroll][narrow]) .no-img .header-info {
          flex-direction: row-reverse;
        }

        :host([scroll][narrow]) .header-info {
          padding: 20px 24px 10px 24px;
          align-items: center;
        }

        :host([scroll]) .header-content {
          align-items: flex-end;
          flex-direction: row;
        }

        :host([scroll]) .header-content .img {
          height: 75px;
          width: 75px;
        }

        :host([scroll][narrow]) .header-content .img {
          height: 100px;
          width: 100px;
          padding-bottom: initial;
          margin-bottom: 0;
        }

        :host([scroll]) ha-fab {
          bottom: 4px;
          right: 4px;
          --mdc-fab-box-shadow: none;
          --mdc-theme-secondary: rgba(var(--rgb-primary-color), 0.5);
        }
        /* AIS css start */
        mwc-list-item {
          display: block;
        }
        mwc-fab.addImageFab {
          position: fixed !important;
          bottom: 16px !important;
          right: 26px !important;
          --mdc-theme-secondary: var(--accent-color) !important;
        }
        mwc-icon-button.aisInfoButton {
          position: relative !important;
        }
        div.aisButtons {
          position: relative;
          width: 100%;
          height: 3em;
          display: flex;
          bottom: 3em;
          margin-bottom: -3em;
          background-color: #9e9e9e8a;
        }
        div.aisButtonsLine {
          float: right;
          position: relative;
        }
        mwc-icon-button.aisButton.aisDeleteButton {
          margin-left: auto;
        }
        mwc-icon-button.aisInfoButton:hover {
          color: var(--primary-color);
        }
        mwc-icon-button.aisEditButton:hover {
          color: var(--primary-color);
        }
        mwc-icon-button.aisDeleteButton:hover {
          color: var(--error-color);
        }
      `]}}]}}),o.oi)},27322:(e,t,i)=>{"use strict";i.d(t,{R:()=>r});const r=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=chunk.6686f7968c43c7bf9e46.js.map