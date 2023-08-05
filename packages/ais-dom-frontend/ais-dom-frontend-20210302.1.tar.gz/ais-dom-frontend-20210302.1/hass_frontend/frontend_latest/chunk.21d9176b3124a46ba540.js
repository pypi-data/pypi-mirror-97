/*! For license information please see chunk.21d9176b3124a46ba540.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6549],{14114:(e,t,r)=>{"use strict";r.d(t,{P:()=>i});const i=e=>(t,r)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,r)=>t.constructor._observers.set(r,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const r=this.constructor._observers.get(t);void 0!==r&&r.call(this,this[t],e)}))}}t.constructor._observers.set(r,e)}},63207:(e,t,r)=>{"use strict";r(65660),r(15112);var i=r(9672),o=r(87156),n=r(50856),s=r(43437);(0,i.k)({_template:n.d`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},15112:(e,t,r)=>{"use strict";r.d(t,{P:()=>o});r(43437);var i=r(9672);class o{constructor(e){o[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return o.types[e]&&o.types[e][t]}set value(e){var t=this.type,r=this.key;t&&r&&(t=o.types[t]=o.types[t]||{},null==e?delete t[r]:t[r]=e)}get list(){if(this.type){var e=o.types[this.type];return e?Object.keys(e).map((function(e){return n[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}o[" "]=function(){},o.types={};var n=o.types;(0,i.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,r){var i=new o({type:e,key:t});return void 0!==r&&r!==i.value?i.value=r:this.value!==i.value&&(this.value=i.value),i},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new o({type:this.type,key:e}).value}})},58993:(e,t,r)=>{"use strict";r.d(t,{yh:()=>i,U2:()=>s,t8:()=>a,ZH:()=>c});class i{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((r,i)=>{const o=indexedDB.open(e,1);o.onerror=()=>i(o.error),o.onsuccess=()=>r(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((r=>new Promise(((i,o)=>{const n=r.transaction(this.storeName,e);n.oncomplete=()=>i(),n.onabort=n.onerror=()=>o(n.error),t(n.objectStore(this.storeName))}))))}}let o;function n(){return o||(o=new i),o}function s(e,t=n()){let r;return t._withIDBStore("readonly",(t=>{r=t.get(e)})).then((()=>r.result))}function a(e,t,r=n()){return r._withIDBStore("readwrite",(r=>{r.put(t,e)}))}function c(e=n()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}},32520:(e,t,r)=>{"use strict";r.r(t);r(81689),r(81545);var i=r(15652),o=r(66386),n=(r(15291),r(60010),r(31206),r(47181)),s=r(11654),a=(r(10983),r(94469)),c=r(55317);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function d(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function v(e,t,r){return(v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(u(n.descriptor)||u(o.descriptor)){if(h(n)||h(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(h(n)){if(h(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}p(n,o)}else t.push(n)}return t}(s.d.map(d)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-config-aiszigbee")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,i.sz)()],key:"_access_token",value:()=>""},{kind:"method",key:"render",value:function(){const e=(0,o.GQ)();this._access_token=null==e?void 0:e.access_token;const t=this.hass.states["sensor.status_serwisu_zigbee2mqtt"];if("online"===t.state){const e=i.dy` <iframe
        src="/api/zigbee2mqtt/${this._access_token}/"
      ></iframe>`;return i.dy`<hass-subpage header="Zigbee2Mqtt" .narrow=${this.narrow}>
        <ha-button-menu corner="BOTTOM_START" slot="toolbar-icon">
          <mwc-icon-button slot="trigger" alt="menu">
            <ha-svg-icon .path=${c.SXi}></ha-svg-icon>
          </mwc-icon-button>
          <mwc-list-item @click=${this._openZigbee2MqttFileConfig}>
            Edit Zigbee2Mqtt configuration.yaml
          </mwc-list-item>
          <mwc-list-item @click=${this._restartZigbeeService}>
            Restart zigbee sevice
          </mwc-list-item>
        </ha-button-menu>
        ${e}
      </hass-subpage>`}return i.dy`<hass-subpage header="Zigbee2Mqtt" .narrow=${this.narrow}>
      <ha-button-menu corner="BOTTOM_START" slot="toolbar-icon">
        <mwc-icon-button slot="trigger" alt="menu">
          <ha-svg-icon .path=${c.SXi}></ha-svg-icon>
        </mwc-icon-button>
        <mwc-list-item @click=${this._openZigbee2MqttFileConfig}>
          Edit Zigbee2Mqtt configuration.yaml
        </mwc-list-item>
        <mwc-list-item @click=${this._restartZigbeeService}>
          Restart Zigbee2Mqtt sevice
        </mwc-list-item>
      </ha-button-menu>
      <div
        style="width: 100%; height: 100%; display: flex; align-items: center;"
      >
        <div style="width: 100%;">
          <p style="text-align: center;">
            <span class="text"><b>BRAK POŁĄCZENIA Z ZIGBEE2MQTT</b></span>
            <span class="icon">
              <svg style="width:24px;height:24px" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M8 2C6.9 2 6 2.9 6 4V12H5V16L9 20V22H15V20L19 16V12H18V4C18 2.9 17.11 2 16 2M8 4H16V12H8M9 7V9H11V7M13 7V9H15V7Z"
                />
              </svg>
            </span>
            <br />
          </p>
          <svg
            style="width:84px;height:84px;display:block;margin:auto;"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M11.6 13V12.9L11.3 12.6H11.2L9.6 12C10 11.7 10.4 11.5 10.9 11.5C11.4 11.5 11.9 11.7 12.3 12.1C12.7 12.5 12.9 12.9 12.9 13.4C12.9 13.9 12.8 14.3 12.4 14.7L11.6 13M9.7 19.3C9.4 18.3 9.6 17.1 10.4 15.5L11.6 18.6C11.8 19.2 11.6 19.6 11 19.9C10.4 20.2 10 20 9.7 19.3M4.1 13.1C4.3 12.5 4.7 12.3 5.3 12.5L8.5 13.7C6.9 14.5 5.7 14.7 4.7 14.4C4.1 14.1 3.9 13.7 4.1 13.1M12 8.1H11V9.5H10.6C9.5 9.5 8.6 9.9 7.8 10.7L7.4 11.3L6 10.5C5.7 10.4 5.4 10.4 5 10.4C4.4 10.4 3.8 10.6 3.3 11S2.4 11.8 2.2 12.4C2 13.1 2 13.7 2.2 14.4C2.5 15.1 2.8 15.6 3.3 15.9C2.9 17.4 3.2 18.7 4.3 19.8C5.1 20.6 6 21 7.1 21C7.6 21 7.9 21 8.2 20.9C8.8 21.7 9.6 22.2 10.6 22.2C10.9 22.2 11.3 22.2 11.6 22.1C12.2 21.9 12.6 21.5 13 21C13.4 20.4 13.6 19.9 13.6 19.3C13.6 18.9 13.6 18.6 13.5 18.3L12.9 16.9L13.5 16.5C14.3 15.7 14.7 14.6 14.6 13.4H16V12.4H14.4C14 11.2 13.2 10.4 12 10V8.1M17.3 6.8C17.1 6.6 17 6.3 17 6.1C17 5.8 17.1 5.6 17.3 5.4C17.5 5.2 17.7 5.1 18 5.1S18.5 5.2 18.7 5.4C18.9 5.5 19 5.8 19 6.1C19 6.4 18.9 6.6 18.7 6.8C18.5 7 18.3 7 18 7S17.5 7 17.3 6.8M20.7 4.1H19.6L19.3 3.2C19.1 2.5 18.7 2.2 18 2.2C17.3 2.2 16.8 2.5 16.7 3.2L16.4 4.1H15.3C14.7 4.1 14.3 4.4 14 5C13.8 5.6 14 6.1 14.6 6.5L15.5 7L15.1 8.2C14.9 8.6 15 9 15.2 9.4C15.5 9.8 15.8 10 16.3 10C16.7 10 17 9.9 17.2 9.7L18 9.1L18.8 9.8C19 9.9 19.3 10 19.7 10C20.2 10 20.5 9.8 20.8 9.4C21 9 21.1 8.6 20.9 8.2L20.5 7L21.3 6.5C21.9 6.1 22.1 5.6 21.9 5C21.7 4.3 21.3 4.1 20.7 4.1Z"
            />
          </svg>
          <p style="text-align: center;">
            <span class="text"
              ><b
                >usługa zigbee2mqtt jest
                <span
                  .onclick="${this.showZigbeeStatus}"
                  style="text-decoration: underline; cursor: pointer;"
                >
                  <a> ${t.state} </a> </span
                >, czekam na połączenie, to może potrwać kilka minut...</b
              ></span
            >
            <br /><br />
            <ha-circular-progress active></ha-circular-progress>
            <br />
            <br />
            W razie problemów sprawdz logi, wpisując w
            <a href="/developer-tools/console">konsoli</a> komendę:
            <b>pm2 logs</b><br />
            Szczegóły w dokumentacji:
            <a href="https://www.ai-speaker.com/docs/ais_app_integration_zigbee"
              >Integracja Zigbee2MQTT</a
            >
          </p>
        </div>
      </div>
    </hass-subpage>`}},{kind:"method",key:"updated",value:function(e){v(g(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"showZigbeeStatus",value:function(){(0,n.B)(this,"hass-more-info",{entityId:"sensor.status_serwisu_zigbee2mqtt"})}},{kind:"method",key:"_openZigbee2MqttFileConfig",value:async function(){const e="/data/data/pl.sviete.dom/files/home/zigbee2mqtt/data/configuration.yaml",t={dialogTitle:"Zigbee2Mqtt configuration.yaml",filePath:e,fileBody:await this.hass.callApi("POST","ais_file/read",{filePath:e}),readonly:!1};(0,a.j)(this,t)}},{kind:"method",key:"_restartZigbeeService",value:async function(){this.hass.callService("ais_shell_command","restart_pm2_service",{service:"zigbee"})}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`
        iframe {
          display: block;
          width: 100%;
          height: 100%;
          border: 0;
        }
        .header + iframe {
          height: calc(100% - 40px);
        }
        .header {
          display: flex;
          align-items: center;
          font-size: 16px;
          height: 40px;
          padding: 0 16px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
          --mdc-icon-size: 20px;
        }

        .main-title {
          margin: 0 0 0 24px;
          line-height: 20px;
          flex-grow: 1;
        }

        mwc-icon-button {
          pointer-events: auto;
        }

        hass-subpage {
          --app-header-background-color: var(--sidebar-background-color);
          --app-header-text-color: var(--sidebar-text-color);
          --app-header-border-bottom: 1px solid var(--divider-color);
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.21d9176b3124a46ba540.js.map