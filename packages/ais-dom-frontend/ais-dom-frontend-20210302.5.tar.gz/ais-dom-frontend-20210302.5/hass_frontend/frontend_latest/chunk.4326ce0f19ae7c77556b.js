/*! For license information please see chunk.4326ce0f19ae7c77556b.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9294],{69470:(e,t,i)=>{"use strict";i.d(t,{j:()=>o,fs:()=>n,$y:()=>s});const r=(e,t,i)=>new Promise(((r,o)=>{const n=document.createElement(e);let s="src",a="body";switch(n.onload=()=>r(t),n.onerror=()=>o(t),e){case"script":n.async=!0,i&&(n.type=i);break;case"link":n.type="text/css",n.rel="stylesheet",s="href",a="head"}n[s]=t,document[a].appendChild(n)})),o=e=>r("link",e),n=e=>r("script",e),s=e=>r("script",e,"module")},41507:(e,t,i)=>{"use strict";i.d(t,{c:()=>r});const r=(e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const r=e[t];r&&(i[r.entity_id]=r)})),i}},36949:(e,t,i)=>{"use strict";i.d(t,{H:()=>n});var r=i(58831),o=i(41507);const n=(e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const n=e[t];if(n&&(i[n.entity_id]=n,"group"===(0,r.M)(n.entity_id))){const t=(0,o.c)(e,n);Object.keys(t).forEach((e=>{const r=t[e];i[e]=r}))}})),i}},33897:(e,t,i)=>{"use strict";i.d(t,{q:()=>o});var r=i(58831);const o=e=>{const t=[],i={};return Object.keys(e).forEach((o=>{const n=e[o];"group"===(0,r.M)(o)?t.push(n):i[o]=n})),t.forEach((e=>e.attributes.entity_id.forEach((e=>{delete i[e]})))),{groups:t,ungrouped:i}}},86977:(e,t,i)=>{"use strict";i.d(t,{Q:()=>r});const r=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},11950:(e,t,i)=>{"use strict";i.d(t,{l:()=>r});const r=async(e,t)=>new Promise((i=>{const r=t(e,(e=>{r(),i(e)}))}))},81545:(e,t,i)=>{"use strict";i(53918),i(42299);var r=i(15652);i(10983);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,u.elements)}),i),u=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(a(n)||a(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(a(n)){if(a(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,u.elements),c.runClassFinishers(h.F,u.finishers)}([(0,r.Mo)("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return r.dy`
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
    `}}]}}),r.oi)},46167:(e,t,i)=>{"use strict";i(87482);var r=i(15652);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function u(e,t,i){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const f=customElements.get("paper-tabs");let m;!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,u.elements)}),i),u=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(a(n)||a(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(a(n)){if(a(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,u.elements),c.runClassFinishers(h.F,u.finishers)}([(0,r.Mo)("ha-tabs")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"_firstTabWidth",value:()=>0},{kind:"field",key:"_lastTabWidth",value:()=>0},{kind:"field",key:"_lastLeftHiddenState",value:()=>!1},{kind:"get",static:!0,key:"template",value:function(){if(!m){m=f.template.cloneNode(!0);const e=m.content.querySelector("style");m.content.querySelectorAll("paper-icon-button").forEach((e=>{e.setAttribute("noink","")})),e.appendChild(document.createTextNode("\n          #selectionBar {\n            box-sizing: border-box;\n          }\n          .not-visible {\n            display: none;\n          }\n          paper-icon-button {\n            width: 24px;\n            height: 48px;\n            padding: 0;\n            margin: 0;\n          }\n        "))}return m}},{kind:"method",key:"_tabChanged",value:function(e,t){u(p(i.prototype),"_tabChanged",this).call(this,e,t);const r=this.querySelectorAll("paper-tab:not(.hide-tab)");r.length>0&&(this._firstTabWidth=r[0].clientWidth,this._lastTabWidth=r[r.length-1].clientWidth);const o=this.querySelector(".iron-selected");o&&o.scrollIntoView()}},{kind:"method",key:"_affectScroll",value:function(e){if(0===this._firstTabWidth||0===this._lastTabWidth)return;this.$.tabsContainer.scrollLeft+=e;const t=this.$.tabsContainer.scrollLeft;this._leftHidden=t-this._firstTabWidth<0,this._rightHidden=t+this._lastTabWidth>this._tabContainerScrollSize,this._lastLeftHiddenState!==this._leftHidden&&(this._lastLeftHiddenState=this._leftHidden,this.$.tabsContainer.scrollLeft+=this._leftHidden?-23:23)}}]}}),f)},57066:(e,t,i)=>{"use strict";i.d(t,{Lo:()=>s,IO:()=>a,qv:()=>l,sG:()=>h});var r=i(95282),o=i(85415),n=i(38346);const s=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),a=(e,t,i)=>e.callWS({type:"config/area_registry/update",area_id:t,...i}),l=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),c=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,t)=>(0,o.q)(e.name,t.name))))),d=(e,t)=>e.subscribeEvents((0,n.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"area_registry_updated"),h=(e,t)=>(0,r.B)("_areaRegistry",c,d,e,t)},57292:(e,t,i)=>{"use strict";i.d(t,{jL:()=>s,y_:()=>a,t1:()=>l,q4:()=>h});var r=i(95282),o=i(91741),n=i(38346);const s=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,r=e.states[t];if(r)return(0,o.C)(r)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device"),a=(e,t)=>e.filter((e=>e.area_id===t)),l=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),c=e=>e.sendMessagePromise({type:"config/device_registry/list"}),d=(e,t)=>e.subscribeEvents((0,n.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),h=(e,t)=>(0,r.B)("_dr",c,d,e,t)},74186:(e,t,i)=>{"use strict";i.d(t,{eD:()=>s,Mw:()=>a,vA:()=>l,L3:()=>c,Nv:()=>d,z3:()=>h,LM:()=>f});var r=i(95282),o=i(91741),n=i(38346);const s=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class)),a=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class)),l=(e,t)=>{if(t.name)return t.name;const i=e.states[t.entity_id];return i?(0,o.C)(i):null},c=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t,i)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...i}),h=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),u=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),p=(e,t)=>e.subscribeEvents((0,n.D)((()=>u(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),f=(e,t)=>(0,r.B)("_entityRegistry",u,p,e,t)},15327:(e,t,i)=>{"use strict";i.d(t,{eL:()=>r,SN:()=>o,id:()=>n,fg:()=>s,j2:()=>a,JR:()=>l,Y:()=>c,iM:()=>d,Q2:()=>h,Oh:()=>u,vj:()=>p,Gc:()=>f});const r=e=>e.sendMessagePromise({type:"lovelace/resources"}),o=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),n=(e,t,i)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...i}),s=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),a=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),c=(e,t,i)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...i}),d=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),h=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i}),u=(e,t,i)=>e.callWS({type:"lovelace/config/save",url_path:t,config:i}),p=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),f=(e,t,i)=>e.subscribeEvents((e=>{e.data.url_path===t&&i()}),"lovelace_updated")},51444:(e,t,i)=>{"use strict";i.d(t,{_:()=>n});var r=i(47181);const o=()=>Promise.all([i.e(5009),i.e(1199),i.e(2420)]).then(i.bind(i,72420)),n=e=>{(0,r.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:o,dialogParams:{}})}},27849:(e,t,i)=>{"use strict";i(39841);var r=i(50856);i(28426);class o extends(customElements.get("app-header-layout")){static get template(){return r.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",o)},7960:(e,t,i)=>{"use strict";i.d(t,{VG:()=>_,UO:()=>x});var r=i(4915),o=i(58831),n=i(27269),s=i(22311),a=i(91741),l=i(49706);var c=i(36949),d=i(33897),h=i(85415),u=i(11950),p=i(7323),f=i(57066),m=i(57292),v=i(74186),y=i(5986),g=i(41499);const b=new Set(["automation","configurator","device_tracker","geo_location","persistent_notification","zone"]),w=new Set(["mobile_app"]);let k=!1;const _=(e,t,i=!1)=>{const r=[],n=[],s=t.title?`${t.title} `:void 0;for(const[t,l]of e){const e=(0,o.M)(t);if("alarm_control_panel"===e){const e={type:"alarm-panel",entity:t};r.push(e)}else if("camera"===e){const e={type:"picture-entity",entity:t};r.push(e)}else if("climate"===e){const e={type:"thermostat",entity:t};r.push(e)}else if("humidifier"===e){const e={type:"humidifier",entity:t};r.push(e)}else if("light"===e&&i){const e={type:"light",entity:t};r.push(e)}else if("media_player"===e){const e={type:"media-control",entity:t};r.push(e)}else if("plant"===e){const e={type:"plant-status",entity:t};r.push(e)}else if("weather"===e){const e={type:"weather-forecast",entity:t,show_forecast:!1};r.push(e)}else if("sensor"===e&&(null==l?void 0:l.attributes.device_class)===g.A);else{let e;const i=s&&l&&(e=(0,a.C)(l)).startsWith(s)?{entity:t,name:E(e.substr(s.length))}:t;n.push(i)}}return n.length>0&&r.unshift({type:"entities",entities:n,...t}),r},E=e=>{return(t=e.substr(0,e.indexOf(" "))).toLowerCase()!==t?e:e[0].toUpperCase()+e.slice(1);var t},C=(e,t,i,r,o,n)=>{const l=(0,d.q)(o);l.groups.sort(((e,t)=>n[e.entity_id]-n[t.entity_id]));const c={};Object.keys(l.ungrouped).forEach((e=>{const t=l.ungrouped[e],i=(0,s.N)(t);i in c||(c[i]=[]),c[i].push(t.entity_id)}));let u=[];l.groups.forEach((e=>{u=u.concat(_(e.attributes.entity_id.map((e=>[e,o[e]])),{title:(0,a.C)(e),show_header_toggle:"hidden"!==e.attributes.control}))})),Object.keys(c).sort().forEach((t=>{u=u.concat(_(c[t].sort(((e,t)=>(0,h.q)((0,a.C)(o[e]),(0,a.C)(o[t])))).map((e=>[e,o[e]])),{title:(0,y.Lh)(e,t)}))}));const p={path:t,title:i,cards:u};return r&&(p.icon=r),p},P=(e,t,i,r,o)=>{const n=((e,t)=>{const i={},r=new Set(t.filter((e=>w.has(e.platform))).map((e=>e.entity_id)));return Object.keys(e).forEach((t=>{const o=e[t];b.has((0,s.N)(o))||r.has(o.entity_id)||(i[t]=e[t])})),i})(r,i),a={};Object.keys(n).forEach((e=>{const t=n[e];t.attributes.order&&(a[e]=t.attributes.order)}));const l=((e,t,i,r)=>{const o={...r},n=[];for(const r of e){const e=[],s=new Set(t.filter((e=>e.area_id===r.area_id)).map((e=>e.id)));for(const t of i)(s.has(t.device_id)&&!t.area_id||t.area_id===r.area_id)&&t.entity_id in o&&(e.push(o[t.entity_id]),delete o[t.entity_id]);e.length>0&&n.push([r,e])}return{areasWithEntities:n,otherEntities:o}})(e,t,i,n),c=C(o,"default_view","Home",undefined,l.otherEntities,a),d=[];return l.areasWithEntities.forEach((([e,t])=>{d.push(..._(t.map((e=>[e.entity_id,e])),{title:e.name}))})),c.cards.unshift(...d),c},$=async(e,t,i,r,o,s)=>{if(e.config.safe_mode)return{title:e.config.location_name,views:[{cards:[{type:"safe-mode"}]}]};const d=(e=>{const t=[];return Object.keys(e).forEach((i=>{const r=e[i];r.attributes.view&&t.push(r)})),t.sort(((e,t)=>e.entity_id===l.a1?-1:t.entity_id===l.a1?1:e.attributes.order-t.attributes.order)),t})(o),h=d.map((e=>{const t=(0,c.H)(o,e),i={};return Object.keys(t).forEach(((e,t)=>{i[e]=t})),C(s,(0,n.p)(e.entity_id),(0,a.C)(e),e.attributes.icon,t,i)}));let u=e.config.location_name;return 0!==d.length&&"group.default_view"===d[0].entity_id||(h.unshift(P(t,i,r,o,s)),(0,p.p)(e,"geo_location")&&h[0]&&h[0].cards&&h[0].cards.push({type:"map",geo_location_sources:["all"]}),h.length>1&&"Home"===u&&(u="Home Assistant")),1===h.length&&0===h[0].cards.length&&h[0].cards.push({type:"empty-state"}),{title:u,views:h}},x=async(e,t)=>{if(e.config.state===r.UE)return{title:e.config.location_name,views:[{cards:[{type:"starting"}]}]};if(e.config.safe_mode)return{title:e.config.location_name,views:[{cards:[{type:"safe-mode"}]}]};k||(k=!0,(0,f.sG)(e.connection,(()=>{})),(0,m.q4)(e.connection,(()=>{})),(0,v.LM)(e.connection,(()=>{})));const[i,o,n]=await Promise.all([(0,u.l)(e.connection,f.sG),(0,u.l)(e.connection,m.q4),(0,u.l)(e.connection,v.LM)]);return $(e,i,o,n,e.states,t||e.localize)}},68500:(e,t,i)=>{"use strict";i.d(t,{k:()=>s});var r=i(69470);const o={},n={},s=(e,t)=>{e.forEach((e=>{const i=new URL(e.url,t).toString();switch(e.type){case"css":if(i in o)break;o[i]=(0,r.j)(i);break;case"js":if(i in n)break;n[i]=(0,r.fs)(i);break;case"module":(0,r.$y)(i);break;default:console.warn(`Unknown resource type specified: ${e.type}`)}}));["/static/ais_dom/cards/card-tools.js?v=20201012","/static/ais_dom/cards/ais-tts.js","/static/ais_dom/cards/lovelace-swipe-navigation.js?v=20201101"].forEach((e=>{const i=new URL(e,t).toString();i in n||(n[i]=(0,r.fs)(i))}));["/static/ais_dom/cards/card-mod.js?v=20201012"].forEach((e=>{(0,r.$y)(new URL(e,t).toString())}))}},89294:(e,t,i)=>{"use strict";i.r(t);i(53918);var r=i(60461),o=i.n(r),n=i(15652),s=i(5986),a=i(15327),l=(i(48811),i(15291),i(81796)),c=i(7960),d=i(68500),h=i(47181);const u="show-save-config";let p=!1;i(81689);var f=i(55317),m=(i(53268),i(11767),i(12730),i(91441),i(87482),i(81471)),v=i(14516),y=i(7323);var g=i(86977),b=i(83849),w=i(87744),k=i(38346),_=i(96151);i(81545),i(16509),i(25230),i(52039);function E(){E=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!$(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return D(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?D(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=z(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:S(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=S(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function C(e){var t,i=z(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function $(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function S(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function z(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function D(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function O(e,t,i){return(O="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=A(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function A(e){return(A=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var o=E();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(x(n.descriptor)||x(o.descriptor)){if($(n)||$(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if($(n)){if($(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}P(n,o)}else t.push(n)}return t}(s.d.map(C)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("ha-icon-button-arrow-next")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_icon",value:()=>f.aIO},{kind:"method",key:"connectedCallback",value:function(){O(A(i.prototype),"connectedCallback",this).call(this),setTimeout((()=>{this._icon="ltr"===window.getComputedStyle(this).direction?f.aIO:f.J3k}),100)}},{kind:"method",key:"render",value:function(){var e;return n.dy`<mwc-icon-button
      .disabled=${this.disabled}
      .label=${this.label||(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.next"))||"Next"}
    >
      <ha-svg-icon .path=${this._icon}></ha-svg-icon>
    </mwc-icon-button> `}}]}}),n.oi);i(2315),i(48932),i(46167);var T=i(26765),j=i(51444),M=(i(27849),i(11654)),R=i(27322),F=i(54324);let I=!1;const L="show-edit-lovelace",V=(e,t)=>{I||(I=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:L,dialogTag:"hui-dialog-edit-lovelace",dialogImport:()=>Promise.all([i.e(5009),i.e(6964),i.e(4764)]).then(i.bind(i,74764))})})(e)),(0,h.B)(e,L,t)};let U=!1;const B="show-edit-view",W=(e,t)=>{U||(U=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:B,dialogTag:"hui-dialog-edit-view",dialogImport:()=>Promise.all([i.e(5009),i.e(2955),i.e(9543),i.e(8374),i.e(2762),i.e(2436),i.e(3098),i.e(6087),i.e(4535),i.e(6902),i.e(7979)]).then(i.bind(i,18632))})})(e)),(0,h.B)(e,B,t)};i(71743);function q(){q=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!Q(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Z(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?Z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=Y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:X(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=X(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function N(e){var t,i=Y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function H(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Q(e){return e.decorators&&e.decorators.length}function G(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function X(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function Y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Z(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function J(e,t,i){return(J="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=K(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function K(e){return(K=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let ee=function(e,t,i,r){var o=q();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(G(n.descriptor)||G(o.descriptor)){if(Q(n)||Q(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(Q(n)){if(Q(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}H(n,o)}else t.push(n)}return t}(s.d.map(N)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._debouncedConfigChanged=(0,k.D)((()=>this._selectView(this._curView,!0)),100,!1)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_curView",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-app-layout",!0)],key:"_appLayout",value:void 0},{kind:"field",key:"_viewCache",value:void 0},{kind:"field",key:"_debouncedConfigChanged",value:void 0},{kind:"field",key:"_conversation",value(){return(0,v.Z)((e=>(0,y.p)(this.hass,"conversation")))}},{kind:"method",key:"render",value:function(){var e,t,i,r;return n.dy`
      <ha-app-layout
        class=${(0,m.$)({"edit-mode":this._editMode})}
        id="layout"
      >
        <app-header slot="header" effects="waterfall" fixed condenses>
          ${this._editMode?n.dy`
                <app-toolbar class="edit-mode">
                  <mwc-icon-button
                    .label="${this.hass.localize("ui.panel.lovelace.menu.exit_edit_mode")}"
                    title="${this.hass.localize("ui.panel.lovelace.menu.close")}"
                    @click="${this._editModeDisable}"
                  >
                    <ha-svg-icon .path=${f.r5M}></ha-svg-icon>
                  </mwc-icon-button>
                  <div main-title>
                    ${this.config.title||this.hass.localize("ui.panel.lovelace.editor.header")}
                    <mwc-icon-button
                      aria-label="${this.hass.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      title="${this.hass.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      class="edit-icon"
                      @click="${this._editLovelace}"
                    >
                      <ha-svg-icon .path=${f.r9}></ha-svg-icon>
                    </mwc-icon-button>
                  </div>
                  <a
                    href="${(0,R.R)(this.hass,"/lovelace/")}"
                    rel="noreferrer"
                    class="menu-link"
                    target="_blank"
                  >
                    <mwc-icon-button
                      title="${this.hass.localize("ui.panel.lovelace.menu.help")}"
                    >
                      <ha-svg-icon .path=${f.Xc_}></ha-svg-icon>
                    </mwc-icon-button>
                  </a>
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .title="${this.hass.localize("ui.panel.lovelace.editor.menu.open")}"
                      .label=${this.hass.localize("ui.panel.lovelace.editor.menu.open")}
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.lAj}
                            >
                            </ha-svg-icon>
                            ${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                          </mwc-list-item>
                        `}
                    <mwc-list-item
                      graphic="icon"
                      @request-selected="${this._handleRawEditor}"
                    >
                      <ha-svg-icon
                        slot="graphic"
                        .path=${f.bl5}
                      ></ha-svg-icon>
                      ${this.hass.localize("ui.panel.lovelace.editor.menu.raw_editor")}
                    </mwc-list-item>
                    ${n.dy`<mwc-list-item
                            graphic="icon"
                            @request-selected="${this._handleManageDashboards}"
                          >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.Ccq}
                            ></ha-svg-icon>
                            ${this.hass.localize("ui.panel.lovelace.editor.menu.manage_dashboards")}
                          </mwc-list-item>
                          ${(null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced)?n.dy`<mwc-list-item
                                graphic="icon"
                                @request-selected="${this._handleManageResources}"
                              >
                                <ha-svg-icon
                                  slot="graphic"
                                  .path=${f.b82}
                                ></ha-svg-icon>
                                ${this.hass.localize("ui.panel.lovelace.editor.menu.manage_resources")}
                              </mwc-list-item>`:""} `}
                  </ha-button-menu>
                </app-toolbar>
              `:n.dy`
                <app-toolbar>
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                  ${this.lovelace.config.views.length>1?n.dy`
                        <ha-tabs
                          scrollable
                          .selected="${this._curView}"
                          @iron-activate="${this._handleViewSelected}"
                          dir="${(0,w.Zu)(this.hass)}"
                        >
                          ${this.lovelace.config.views.map((e=>n.dy`
                              <paper-tab
                                aria-label="${e.title}"
                                class="${(0,m.$)({"hide-tab":Boolean(void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.hass.user.id))||!1===e.visible))})}"
                              >
                                ${e.icon?n.dy`
                                      <ha-icon
                                        title="${e.title}"
                                        .icon="${e.icon}"
                                      ></ha-icon>
                                    `:e.title||"Unnamed view"}
                              </paper-tab>
                            `))}
                        </ha-tabs>
                      `:n.dy`<div main-title>${this.config.title}</div>`}
                  ${!this.narrow&&this._conversation(this.hass.config.components)?n.dy`
                        <mwc-icon-button
                          .label=${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}
                          @click=${this._showVoiceCommandDialog}
                        >
                          <ha-svg-icon .path=${f.N3O}></ha-svg-icon>
                        </mwc-icon-button>
                      `:""}
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .label=${this.hass.localize("ui.panel.lovelace.editor.menu.open")}
                      .title="${this.hass.localize("ui.panel.lovelace.editor.menu.open")}"
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${this.narrow&&this._conversation(this.hass.config.components)?n.dy`
                          <mwc-list-item
                            .label=${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}
                            graphic="icon"
                            @request-selected=${this._showVoiceCommandDialog}
                          >
                            <span
                              >${this.hass.localize("ui.panel.lovelace.menu.start_conversation")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.N3O}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${this._yamlMode?n.dy`
                          <mwc-list-item
                            aria-label=${this.hass.localize("ui.common.refresh")}
                            graphic="icon"
                            @request-selected="${this._handleRefresh}"
                          >
                            <span
                              >${this.hass.localize("ui.common.refresh")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                          <mwc-list-item
                            aria-label=${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
                            graphic="icon"
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            <span
                              >${this.hass.localize("ui.panel.lovelace.unused_entities.title")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.RIj}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${"yaml"===(null===(t=this.hass.panels.lovelace)||void 0===t||null===(i=t.config)||void 0===i?void 0:i.mode)?n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.hass.localize("ui.panel.lovelace.menu.reload_resources")}
                            @request-selected=${this._handleReloadResources}
                          >
                            ${this.hass.localize("ui.panel.lovelace.menu.reload_resources")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${(null===(r=this.hass.user)||void 0===r?void 0:r.is_admin)&&!this.hass.config.safe_mode?n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.hass.localize("ui.panel.lovelace.menu.configure_ui")}
                            @request-selected=${this._handleEnableEditMode}
                          >
                            ${this.hass.localize("ui.panel.lovelace.menu.configure_ui")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.Shd}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    <a
                      href="${(0,R.R)(this.hass,"/lovelace/")}"
                      rel="noreferrer"
                      class="menu-link"
                      target="_blank"
                    >
                      <mwc-list-item
                        graphic="icon"
                        aria-label=${this.hass.localize("ui.panel.lovelace.menu.help")}
                      >
                        ${this.hass.localize("ui.panel.lovelace.menu.help")}
                        <ha-svg-icon
                          slot="graphic"
                          .path=${f.HET}
                        ></ha-svg-icon>
                      </mwc-list-item>
                    </a>
                  </ha-button-menu>
                </app-toolbar>
              `}
          ${this._editMode?n.dy`
                <div sticky>
                  <paper-tabs
                    scrollable
                    .selected="${this._curView}"
                    @iron-activate="${this._handleViewSelected}"
                    dir="${(0,w.Zu)(this.hass)}"
                  >
                    ${this.lovelace.config.views.map((e=>n.dy`
                        <paper-tab
                          aria-label="${e.title}"
                          class="${(0,m.$)({"hide-tab":Boolean(!this._editMode&&void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.hass.user.id))||!1===e.visible))})}"
                        >
                          ${this._editMode?n.dy`
                                <ha-icon-button-arrow-prev
                                  .hass=${this.hass}
                                  .title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_left")}"
                                  .label="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_left")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewLeft}"
                                  ?disabled="${0===this._curView}"
                                ></ha-icon-button-arrow-prev>
                              `:""}
                          ${e.icon?n.dy`
                                <ha-icon
                                  title="${e.title}"
                                  .icon="${e.icon}"
                                ></ha-icon>
                              `:e.title||"Unnamed view"}
                          ${this._editMode?n.dy`
                                <ha-svg-icon
                                  title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.edit")}"
                                  class="edit-icon view"
                                  .path=${f.r9}
                                  @click="${this._editView}"
                                ></ha-svg-icon>
                                <ha-icon-button-arrow-next
                                  .hass=${this.hass}
                                  .title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_right")}"
                                  .label="${this.hass.localize("ui.panel.lovelace.editor.edit_view.move_right")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewRight}"
                                  ?disabled="${this._curView+1===this.lovelace.config.views.length}"
                                ></ha-icon-button-arrow-next>
                              `:""}
                        </paper-tab>
                      `))}
                    ${this._editMode?n.dy`
                          <mwc-icon-button
                            id="add-view"
                            @click="${this._addView}"
                            title="${this.hass.localize("ui.panel.lovelace.editor.edit_view.add")}"
                          >
                            <ha-svg-icon .path=${f.qX5}></ha-svg-icon>
                          </mwc-icon-button>
                        `:""}
                  </paper-tabs>
                </div>
              `:""}
        </app-header>
        <div id="view" @ll-rebuild="${this._debouncedConfigChanged}"></div>
      </ha-app-layout>
    `}},{kind:"field",key:"_isVisible",value(){return e=>Boolean(this._editMode||void 0===e.visible||!0===e.visible||Array.isArray(e.visible)&&e.visible.some((e=>{var t;return e.user===(null===(t=this.hass.user)||void 0===t?void 0:t.id)})))}},{kind:"method",key:"updated",value:function(e){J(K(r.prototype),"updated",this).call(this,e);const t=this._viewRoot.lastChild;let i;e.has("hass")&&t&&(t.hass=this.hass),e.has("narrow")&&t&&(t.narrow=this.narrow);let o=!1;const n=this.route.path.split("/")[1];if(e.has("route")){const e=this.config.views;if(!n&&e.length)i=e.findIndex(this._isVisible),(0,b.c)(this,`${this.route.prefix}/${e[i].path||i}`,!0);else if("hass-unused-entities"===n)i="hass-unused-entities";else if(n){const t=n,r=Number(t);let o=0;for(let i=0;i<e.length;i++)if(e[i].path===t||i===r){o=i;break}i=o}}if(e.has("lovelace")){const r=e.get("lovelace");if(r&&r.config===this.lovelace.config||(o=!0),!r||r.editMode!==this.lovelace.editMode){const e=this.config&&this.config.views;(0,h.B)(this,"iron-resize"),"storage"===this.lovelace.mode&&"hass-unused-entities"===n&&(i=e.findIndex(this._isVisible),(0,b.c)(this,`${this.route.prefix}/${e[i].path||i}`,!0))}!o&&t&&(t.lovelace=this.lovelace)}(void 0!==i||o)&&(o&&void 0===i&&(i=this._curView),(0,_.T)((()=>this._selectView(i,o))))}},{kind:"get",key:"config",value:function(){return this.lovelace.config}},{kind:"get",key:"_yamlMode",value:function(){return"yaml"===this.lovelace.mode}},{kind:"get",key:"_editMode",value:function(){return this.lovelace.editMode}},{kind:"get",key:"_layout",value:function(){return this.shadowRoot.getElementById("layout")}},{kind:"get",key:"_viewRoot",value:function(){return this.shadowRoot.getElementById("view")}},{kind:"method",key:"_handleRefresh",value:function(e){(0,g.Q)(e)&&(0,h.B)(this,"config-refresh")}},{kind:"method",key:"_handleReloadResources",value:function(e){(0,g.Q)(e)&&(this.hass.callService("lovelace","reload_resources"),(0,T.g7)(this,{title:this.hass.localize("ui.panel.lovelace.reload_resources.refresh_header"),text:this.hass.localize("ui.panel.lovelace.reload_resources.refresh_body"),confirmText:this.hass.localize("ui.common.refresh"),dismissText:this.hass.localize("ui.common.not_now"),confirm:()=>location.reload()}))}},{kind:"method",key:"_handleRawEditor",value:function(e){(0,g.Q)(e)&&this.lovelace.enableFullEditMode()}},{kind:"method",key:"_handleManageDashboards",value:function(e){(0,g.Q)(e)&&(0,b.c)(this,"/config/lovelace/dashboards")}},{kind:"method",key:"_handleManageResources",value:function(e){(0,g.Q)(e)&&(0,b.c)(this,"/config/lovelace/resources")}},{kind:"method",key:"_handleUnusedEntities",value:function(e){var t;(0,g.Q)(e)&&(0,b.c)(this,`${null===(t=this.route)||void 0===t?void 0:t.prefix}/hass-unused-entities`)}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,j._)(this)}},{kind:"method",key:"_handleEnableEditMode",value:function(e){(0,g.Q)(e)&&(this._yamlMode?(0,T.Ys)(this,{text:"The edit UI is not available when in YAML mode."}):this._enableEditMode())}},{kind:"method",key:"_enableEditMode",value:function(){this.lovelace.setEditMode(!0)}},{kind:"method",key:"_editModeDisable",value:function(){this.lovelace.setEditMode(!1)}},{kind:"method",key:"_editLovelace",value:function(){V(this,this.lovelace)}},{kind:"method",key:"_editView",value:function(){W(this,{lovelace:this.lovelace,viewIndex:this._curView})}},{kind:"method",key:"_moveViewLeft",value:function(){if(0===this._curView)return;const e=this.lovelace,t=this._curView,i=this._curView-1;this._curView=i,e.saveConfig((0,F.mA)(e.config,t,i))}},{kind:"method",key:"_moveViewRight",value:function(){if(this._curView+1===this.lovelace.config.views.length)return;const e=this.lovelace,t=this._curView,i=this._curView+1;this._curView=i,e.saveConfig((0,F.mA)(e.config,t,i))}},{kind:"method",key:"_addView",value:function(){W(this,{lovelace:this.lovelace,saveCallback:(e,t)=>{var i;const r=t.path||e;(0,b.c)(this,`${null===(i=this.route)||void 0===i?void 0:i.prefix}/${r}`)}})}},{kind:"method",key:"_handleViewSelected",value:function(e){const t=e.detail.selected;if(t!==this._curView){var i;const e=this.config.views[t].path||t;(0,b.c)(this,`${null===(i=this.route)||void 0===i?void 0:i.prefix}/${e}`)}!function(e,t){const i=t,r=Math.random(),o=Date.now(),n=i.scrollTop,s=0-n;e._currentAnimationId=r,function t(){const a=Date.now()-o;var l;a>200?i.scrollTop=0:e._currentAnimationId===r&&(i.scrollTop=(l=a,-s*(l/=200)*(l-2)+n),requestAnimationFrame(t.bind(e)))}.call(e)}(this,this._layout.header.scrollTarget)}},{kind:"method",key:"_selectView",value:function(e,t){if(!t&&this._curView===e)return;e=void 0===e?0:e,this._curView=e,t&&(this._viewCache={});const r=this._viewRoot;if(r.lastChild&&r.removeChild(r.lastChild),"hass-unused-entities"===e){const e=document.createElement("hui-unused-entities");return Promise.all([i.e(3330),i.e(2098),i.e(9395),i.e(7065),i.e(8279)]).then(i.bind(i,28279)).then((()=>{e.hass=this.hass,e.lovelace=this.lovelace,e.narrow=this.narrow})),void r.appendChild(e)}let o;const n=this.config.views[e];if(!n)return void this._enableEditMode();!t&&this._viewCache[e]?o=this._viewCache[e]:(o=document.createElement("hui-view"),o.index=e,this._viewCache[e]=o),o.lovelace=this.lovelace,o.hass=this.hass,o.narrow=this.narrow;const s=n.background||this.config.background;s?this._appLayout.style.setProperty("--lovelace-background",s):this._appLayout.style.removeProperty("--lovelace-background"),r.appendChild(o),(0,h.B)(this,"iron-resize")}},{kind:"get",static:!0,key:"styles",value:function(){return[M.Qx,n.iv`
        :host {
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
        }

        ha-app-layout {
          min-height: 100%;
        }
        ha-tabs {
          width: 100%;
          height: 100%;
          margin-left: 4px;
        }
        paper-tabs {
          margin-left: 12px;
          margin-left: max(env(safe-area-inset-left), 12px);
          margin-right: env(safe-area-inset-right);
        }
        ha-tabs,
        paper-tabs {
          --paper-tabs-selection-bar-color: var(
            --app-header-selection-bar-color,
            var(--app-header-text-color, #fff)
          );
          text-transform: uppercase;
        }

        .edit-mode app-header,
        .edit-mode app-toolbar {
          background-color: var(--app-header-edit-background-color, #455a64);
          color: var(--app-header-edit-text-color, #fff);
        }
        .edit-mode div[main-title] {
          pointer-events: auto;
        }
        paper-tab.iron-selected .edit-icon {
          display: inline-flex;
        }
        .edit-icon {
          color: var(--accent-color);
          padding-left: 8px;
          vertical-align: middle;
          --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
        }
        .edit-icon.view {
          display: none;
        }
        #add-view {
          position: absolute;
          height: 44px;
        }
        #add-view ha-svg-icon {
          background-color: var(--accent-color);
          border-radius: 4px;
        }
        app-toolbar a {
          color: var(--text-primary-color, white);
        }
        mwc-button.warning:not([disabled]) {
          color: var(--error-color);
        }
        #view {
          min-height: calc(100vh - var(--header-height));
          /**
          * Since we only set min-height, if child nodes need percentage
          * heights they must use absolute positioning so we need relative
          * positioning here.
          *
          * https://www.w3.org/TR/CSS2/visudet.html#the-height-property
          */
          position: relative;
          display: flex;
        }
        /**
         * In edit mode we have the tab bar on a new line *
         */
        .edit-mode #view {
          min-height: calc(100vh - var(--header-height) - 48px);
        }
        #view > * {
          /**
          * The view could get larger than the window in Firefox
          * to prevent that we set the max-width to 100%
          * flex-grow: 1 and flex-basis: 100% should make sure the view
          * stays full width.
          *
          * https://github.com/home-assistant/home-assistant-polymer/pull/3806
          */
          flex: 1 1 100%;
          max-width: 100%;
        }
        .hide-tab {
          display: none;
        }
        .menu-link {
          text-decoration: none;
        }
        hui-view {
          background: var(
            --lovelace-background,
            var(--primary-background-color)
          );
        }
      `]}}]}}),n.oi);function te(){te=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!oe(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return le(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?le(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=ae(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:se(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=se(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function ie(e){var t,i=ae(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function re(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function oe(e){return e.decorators&&e.decorators.length}function ne(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function se(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function ae(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function le(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function ce(e,t,i){return(ce="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=de(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function de(e){return(de=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}customElements.define("hui-root",ee),window.loadCardHelpers=()=>Promise.all([i.e(4909),i.e(319),i.e(7282),i.e(9810),i.e(5457)]).then(i.bind(i,49686));let he=!1,ue=!1,pe=function(e,t,i,r){var o=te();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(ne(n.descriptor)||ne(o.descriptor)){if(oe(n)||oe(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(oe(n)){if(oe(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}re(n,o)}else t.push(n)}return t}(s.d.map(ie)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._closeEditor=this._closeEditor.bind(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"panel",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_state",value:()=>"loading"},{kind:"field",decorators:[(0,n.sz)()],key:"_errorMsg",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"lovelace",value:void 0},{kind:"field",key:"_ignoreNextUpdateEvent",value:()=>!1},{kind:"field",key:"_fetchConfigOnConnect",value:()=>!1},{kind:"field",key:"_unsubUpdates",value:void 0},{kind:"method",key:"connectedCallback",value:function(){ce(de(r.prototype),"connectedCallback",this).call(this),this.lovelace&&this.hass&&this.lovelace.language!==this.hass.language?this._setLovelaceConfig(this.lovelace.config,this.lovelace.mode):this.lovelace&&"generated"===this.lovelace.mode?(this._state="loading",this._regenerateConfig()):this._fetchConfigOnConnect&&this._fetchConfig(!1)}},{kind:"method",key:"disconnectedCallback",value:function(){ce(de(r.prototype),"disconnectedCallback",this).call(this),null!==this.urlPath&&this._unsubUpdates&&this._unsubUpdates()}},{kind:"method",key:"render",value:function(){const e=this._state;return"loaded"===e?n.dy`
        <hui-root
          .hass=${this.hass}
          .lovelace=${this.lovelace}
          .route=${this.route}
          .narrow=${this.narrow}
          @config-refresh=${this._forceFetchConfig}
        ></hui-root>
      `:"error"===e?n.dy`
        <hass-error-screen
          .hass=${this.hass}
          title="${(0,s.Lh)(this.hass.localize,"lovelace")}"
          .error="${this._errorMsg}"
        >
          <mwc-button raised @click=${this._forceFetchConfig}>
            ${this.hass.localize("ui.panel.lovelace.reload_lovelace")}
          </mwc-button>
        </hass-error-screen>
      `:"yaml-editor"===e?n.dy`
        <hui-editor
          .hass=${this.hass}
          .lovelace="${this.lovelace}"
          .closeEditor="${this._closeEditor}"
        ></hui-editor>
      `:n.dy`
      <hass-loading-screen
        rootnav
        .hass=${this.hass}
        .narrow=${this.narrow}
      ></hass-loading-screen>
    `}},{kind:"method",key:"firstUpdated",value:function(){this._fetchConfig(!1),this._unsubUpdates||this._subscribeUpdates(),window.addEventListener("connection-status",(e=>{"connected"===e.detail&&this._fetchConfig(!1)}))}},{kind:"method",key:"_regenerateConfig",value:async function(){const e=await(0,c.UO)(this.hass);this._setLovelaceConfig(e,"generated"),this._state="loaded"}},{kind:"method",key:"_subscribeUpdates",value:async function(){this._unsubUpdates=await(0,a.Gc)(this.hass.connection,this.urlPath,(()=>this._lovelaceChanged()))}},{kind:"method",key:"_closeEditor",value:function(){this._state="loaded"}},{kind:"method",key:"_lovelaceChanged",value:function(){this._ignoreNextUpdateEvent?this._ignoreNextUpdateEvent=!1:this.isConnected?(0,l.C)(this,{message:this.hass.localize("ui.panel.lovelace.changed_toast.message"),action:{action:()=>this._fetchConfig(!1),text:this.hass.localize("ui.common.refresh")},duration:0,dismissable:!1}):this._fetchConfigOnConnect=!0}},{kind:"get",key:"urlPath",value:function(){return"lovelace"===this.panel.url_path?null:this.panel.url_path}},{kind:"method",key:"_forceFetchConfig",value:function(){this._fetchConfig(!0)}},{kind:"method",key:"_fetchConfig",value:async function(e){let t,i,r=this.panel.config.mode;const o=window;o.llConfProm&&(i=o.llConfProm,o.llConfProm=void 0),ue||(ue=!0,(o.llConfProm||(0,a.eL)(this.hass.connection)).then((e=>(0,d.k)(e,this.hass.auth.data.hassUrl)))),null===this.urlPath&&i||(this.lovelace&&"yaml"===this.lovelace.mode&&(this._ignoreNextUpdateEvent=!0),i=(0,a.Q2)(this.hass.connection,this.urlPath,e));try{t=await i}catch(e){if("config_not_found"!==e.code)return console.log(e),this._state="error",void(this._errorMsg=e.message);const i=await this.hass.loadBackendTranslation("title");t=await(0,c.UO)(this.hass,i),r="generated"}finally{this.lovelace&&"yaml"===this.lovelace.mode&&setTimeout((()=>{this._ignoreNextUpdateEvent=!1}),2e3)}this._state="yaml-editor"===this._state?this._state:"loaded",this._setLovelaceConfig(t,r)}},{kind:"method",key:"_checkLovelaceConfig",value:function(e){let t=Object.isFrozen(e)?void 0:e;return e.views.forEach(((i,r)=>{i.badges&&!i.badges.every(Boolean)&&(t=t||{...e,views:[...e.views]},t.views[r]={...i},t.views[r].badges=i.badges.filter(Boolean))})),t?o()(t):e}},{kind:"method",key:"_setLovelaceConfig",value:function(e,t){e=this._checkLovelaceConfig(e);const r=this.urlPath;this.lovelace={config:e,mode:t,urlPath:this.urlPath,editMode:!!this.lovelace&&this.lovelace.editMode,language:this.hass.language,enableFullEditMode:()=>{he||(he=!0,Promise.all([i.e(9033),i.e(3304),i.e(2118),i.e(5912)]).then(i.bind(i,95912))),this._state="yaml-editor"},setEditMode:e=>{var t,r;e&&"generated"===this.lovelace.mode?(t=this,r={lovelace:this.lovelace,mode:this.panel.config.mode},p||(p=!0,(0,h.B)(t,"register-dialog",{dialogShowEvent:u,dialogTag:"hui-dialog-save-config",dialogImport:()=>Promise.all([i.e(2762),i.e(2436),i.e(9033),i.e(3304),i.e(8082)]).then(i.bind(i,78082))})),(0,h.B)(t,u,r)):this._updateLovelace({editMode:e})},saveConfig:async e=>{const{config:t,mode:i}=this.lovelace;e=this._checkLovelaceConfig(e);try{this._updateLovelace({config:e,mode:"storage"}),this._ignoreNextUpdateEvent=!0,await(0,a.Oh)(this.hass,r,e)}catch(e){throw console.error(e),this._updateLovelace({config:t,mode:i}),e}},deleteConfig:async()=>{const{config:e,mode:t}=this.lovelace;try{const e=await this.hass.loadBackendTranslation("title");this._updateLovelace({config:await(0,c.UO)(this.hass,e),mode:"generated",editMode:!1}),this._ignoreNextUpdateEvent=!0,await(0,a.vj)(this.hass,r)}catch(i){throw console.error(i),this._updateLovelace({config:e,mode:t}),i}}}}},{kind:"method",key:"_updateLovelace",value:function(e){this.lovelace={...this.lovelace,...e}}}]}}),n.oi);customElements.define("ha-panel-lovelace",pe)},27322:(e,t,i)=>{"use strict";i.d(t,{R:()=>r});const r=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=chunk.4326ce0f19ae7c77556b.js.map