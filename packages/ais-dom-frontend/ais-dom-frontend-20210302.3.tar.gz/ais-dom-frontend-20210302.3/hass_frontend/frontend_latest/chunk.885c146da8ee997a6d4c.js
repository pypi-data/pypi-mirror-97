/*! For license information please see chunk.885c146da8ee997a6d4c.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3895],{63207:(e,t,i)=>{"use strict";i(65660),i(15112);var n=i(9672),s=i(87156),o=i(50856),r=i(43437);(0,n.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:r.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,s.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,s.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{"use strict";i.d(t,{P:()=>s});i(43437);var n=i(9672);class s{constructor(e){s[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return s.types[e]&&s.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=s.types[t]=s.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=s.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}s[" "]=function(){},s.types={};var o=s.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var n=new s({type:e,key:t});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new s({type:this.type,key:e}).value}})},25782:(e,t,i)=>{"use strict";i(43437),i(65660),i(70019),i(97968);var n=i(9672),s=i(50856),o=i(33760);(0,n.k)({_template:s.d`
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
`,is:"paper-icon-item",behaviors:[o.U]})},33760:(e,t,i)=>{"use strict";i.d(t,{U:()=>o});i(43437);var n=i(51644),s=i(26110);const o=[n.P,s.a,{hostAttributes:{role:"option",tabindex:"0"}}]},97968:(e,t,i)=>{"use strict";i(65660),i(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(e,t,i)=>{"use strict";i(43437),i(65660),i(97968);var n=i(9672),s=i(50856),o=i(33760);(0,n.k)({_template:s.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[o.U]})},51095:(e,t,i)=>{"use strict";i(43437);var n=i(78161),s=i(9672),o=i(50856);(0,s.k)({_template:o.d`
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
`,is:"paper-listbox",behaviors:[n.i],hostAttributes:{role:"listbox"}})},58993:(e,t,i)=>{"use strict";i.d(t,{yh:()=>n,U2:()=>r,t8:()=>a,ZH:()=>p});class n{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((i,n)=>{const s=indexedDB.open(e,1);s.onerror=()=>n(s.error),s.onsuccess=()=>i(s.result),s.onupgradeneeded=()=>{s.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((i=>new Promise(((n,s)=>{const o=i.transaction(this.storeName,e);o.oncomplete=()=>n(),o.onabort=o.onerror=()=>s(o.error),t(o.objectStore(this.storeName))}))))}}let s;function o(){return s||(s=new n),s}function r(e,t=o()){let i;return t._withIDBStore("readonly",(t=>{i=t.get(e)})).then((()=>i.result))}function a(e,t,i=o()){return i._withIDBStore("readwrite",(i=>{i.put(t,e)}))}function p(e=o()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}},1275:(e,t,i)=>{"use strict";i.d(t,{l:()=>o});var n=i(94707);const s=new WeakMap,o=(0,n.XM)(((e,t)=>i=>{const n=s.get(i);if(Array.isArray(e)){if(Array.isArray(n)&&n.length===e.length&&e.every(((e,t)=>e===n[t])))return}else if(n===e&&(void 0!==e||s.has(i)))return;i.setValue(t()),s.set(i,Array.isArray(e)?Array.from(e):e)}))}}]);
//# sourceMappingURL=chunk.885c146da8ee997a6d4c.js.map