/*! For license information please see chunk.9a67ae1955c87080b248.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8335],{14114:(e,t,n)=>{"use strict";n.d(t,{P:()=>o});const o=e=>(t,n)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,n)=>t.constructor._observers.set(n,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const n=this.constructor._observers.get(t);void 0!==n&&n.call(this,this[t],e)}))}}t.constructor._observers.set(n,e)}},8878:(e,t,n)=>{"use strict";n(43437),n(8621),n(63207),n(30879),n(78814),n(60748),n(57548),n(73962);var o=n(51644),r=n(26110),i=n(21006),s=n(98235),a=n(9672),l=n(87156),c=n(81668),p=n(50856);(0,a.k)({_template:p.d`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[o.P,r.a,i.V,s.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,l.vz)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},25782:(e,t,n)=>{"use strict";n(43437),n(65660),n(70019),n(97968);var o=n(9672),r=n(50856),i=n(33760);(0,o.k)({_template:r.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.U]})},51095:(e,t,n)=>{"use strict";n(43437);var o=n(78161),r=n(9672),i=n(50856);(0,r.k)({_template:i.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[o.i],hostAttributes:{role:"listbox"}})},4268:(e,t,n)=>{"use strict";function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},i=Object.keys(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}function*a(e,t){!0===e||(!1===e?yield t.fail():yield*e)}function l(e){const{done:t,value:n}=e.next();return t?void 0:n}n.d(t,{DD:()=>p,Yj:()=>h,IX:()=>b,hu:()=>u,O7:()=>v,D8:()=>m,kE:()=>g,i0:()=>O,Rx:()=>_,Ry:()=>j,jt:()=>k,Z_:()=>x,n_:()=>S,dt:()=>A,G0:()=>I});class c{constructor(e){const{type:t,schema:n,coercer:o=(e=>e),validator:r=(()=>[]),refiner:i=(()=>[])}=e;this.type=t,this.schema=n,this.coercer=o,this.validator=r,this.refiner=i}}class p extends TypeError{constructor(e,t){const{path:n,value:o,type:r,branch:i}=e,a=s(e,["path","value","type","branch"]);let l;super(`Expected a value of type \`${r}\`${n.length?` for \`${n.join(".")}\``:""} but received \`${JSON.stringify(o)}\`.`),this.value=o,Object.assign(this,a),this.type=r,this.path=n,this.branch=i,this.failures=function(){return l||(l=[e,...t]),l},this.stack=(new Error).stack,this.__proto__=p.prototype}}function u(e,t){const n=f(e,t);if(n[0])throw n[0]}function d(e,t){const n=t.coercer(e);return u(n,t),n}function f(e,t,n=!1){n&&(e=t.coercer(e));const o=y(e,t),r=l(o);if(r){return[new p(r,o),void 0]}return[void 0,e]}function*y(e,t,n=[],o=[]){const{type:r}=t,s={value:e,type:r,branch:o,path:n,fail:(t={})=>i({value:e,type:r,path:n,branch:[...o,e]},t),check:(e,t,r,i)=>y(e,t,void 0!==r?[...n,i]:n,void 0!==r?[...o,r]:o)},c=a(t.validator(e,s),s),p=l(c);p?(yield p,yield*c):yield*a(t.refiner(e,s),s)}function h(){return S("any",(()=>!0))}function b(e){return new c({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map((t=>d(t,e))):t,*validator(t,n){if(Array.isArray(t)){if(e)for(const[o,r]of t.entries())yield*n.check(r,e,t,o)}else yield n.fail()}})}function v(){return S("boolean",(e=>"boolean"==typeof e))}function m(e){return S("Dynamic<...>",((t,n)=>n.check(t,e(t,n))))}function g(e){return S(`Enum<${e.map(E)}>`,(t=>e.includes(t)))}function O(e){return S(`Literal<${E(e)}>`,(t=>t===e))}function w(){return S("never",(()=>!1))}function _(){return S("number",(e=>"number"==typeof e&&!isNaN(e)))}function j(e){const t=e?Object.keys(e):[],n=w();return new c({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?$(e):e=>e,*validator(o,r){if("object"==typeof o&&null!=o){if(e){const i=new Set(Object.keys(o));for(const n of t){i.delete(n);const t=e[n],s=o[n];yield*r.check(s,t,o,n)}for(const e of i){const t=o[e];yield*r.check(t,n,o,e)}}}else yield r.fail()}})}function k(e){return new c({type:`${e.type}?`,schema:e.schema,validator:(t,n)=>void 0===t||n.check(t,e)})}function x(){return S("string",(e=>"string"==typeof e))}function S(e,t){return new c({type:e,validator:t,schema:null})}function A(e){const t=Object.keys(e);return S(`Type<{${t.join(",")}}>`,(function*(n,o){if("object"==typeof n&&null!=n)for(const r of t){const t=e[r],i=n[r];yield*o.check(i,t,n,r)}else yield o.fail()}))}function I(e){return S(`${e.map((e=>e.type)).join(" | ")}`,(function*(t,n){for(const o of e){const[...e]=n.check(t,o);if(0===e.length)return}yield n.fail()}))}function E(e){return"string"==typeof e?`"${e.replace(/"/g,'"')}"`:`${e}`}function $(e){const t=Object.keys(e);return n=>{if("object"!=typeof n||null==n)return n;const o={},r=new Set(Object.keys(n));for(const i of t){r.delete(i);const t=e[i],s=n[i];o[i]=d(s,t)}for(const e of r)o[e]=n[e];return o}}}}]);
//# sourceMappingURL=chunk.9a67ae1955c87080b248.js.map