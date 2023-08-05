/*! For license information please see chunk.530fab37cbe6c9b6d043.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3245],{63207:(e,t,i)=>{"use strict";i(65660),i(15112);var n=i(9672),o=i(87156),r=i(50856),a=i(43437);(0,n.k)({_template:r.d`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:a.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{"use strict";i.d(t,{P:()=>o});i(43437);var n=i(9672);class o{constructor(e){o[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return o.types[e]&&o.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=o.types[t]=o.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=o.types[this.type];return e?Object.keys(e).map((function(e){return r[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}o[" "]=function(){},o.types={};var r=o.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var n=new o({type:e,key:t});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new o({type:this.type,key:e}).value}})},58993:(e,t,i)=>{"use strict";i.d(t,{yh:()=>n,U2:()=>a,t8:()=>s,ZH:()=>c});class n{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((i,n)=>{const o=indexedDB.open(e,1);o.onerror=()=>n(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((i=>new Promise(((n,o)=>{const r=i.transaction(this.storeName,e);r.oncomplete=()=>n(),r.onabort=r.onerror=()=>o(r.error),t(r.objectStore(this.storeName))}))))}}let o;function r(){return o||(o=new n),o}function a(e,t=r()){let i;return t._withIDBStore("readonly",(t=>{i=t.get(e)})).then((()=>i.result))}function s(e,t,i=r()){return i._withIDBStore("readwrite",(i=>{i.put(t,e)}))}function c(e=r()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}},27269:(e,t,i)=>{"use strict";i.d(t,{p:()=>n});const n=e=>e.substr(e.indexOf(".")+1)},91741:(e,t,i)=>{"use strict";i.d(t,{C:()=>o});var n=i(27269);const o=e=>void 0===e.attributes.friendly_name?(0,n.p)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},85415:(e,t,i)=>{"use strict";i.d(t,{q:()=>n,w:()=>o});const n=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>n(e.toLowerCase(),t.toLowerCase())},73728:(e,t,i)=>{"use strict";i.d(t,{pV:()=>a,P3:()=>s,Ky:()=>l,D4:()=>d,XO:()=>h,zO:()=>p,oi:()=>u,d4:()=>f,D7:()=>m,ZJ:()=>g,V3:()=>y,WW:()=>w});var n=i(95282),o=i(38346),r=i(5986);const a=["unignore","dhcp","homekit","ssdp","zeroconf","discovery","mqtt"],s=["reauth"],c={"HA-Frontend-Base":`${location.protocol}//${location.host}`},l=(e,t)=>{var i;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(i=e.userData)||void 0===i?void 0:i.showAdvanced)},c)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,c),h=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,c),p=(e,t,i)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:i}),u=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),f=e=>e.callApi("GET","config/config_entries/flow_handlers"),m=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),v=(e,t)=>e.subscribeEvents((0,o.D)((()=>m(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),g=e=>(0,n._)(e,"_configFlowProgress",m,v),y=(e,t)=>g(e.connection).subscribe(t),w=(e,t)=>{const i=t.context.title_placeholders||{},n=Object.keys(i);if(0===n.length)return(0,r.Lh)(e,t.handler);const o=[];return n.forEach((e=>{o.push(e),o.push(i[e])})),e(`component.${t.handler}.config.flow_title`,...o)}},57292:(e,t,i)=>{"use strict";i.d(t,{jL:()=>a,y_:()=>s,t1:()=>c,q4:()=>h});var n=i(95282),o=i(91741),r=i(38346);const a=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,n=e.states[t];if(n)return(0,o.C)(n)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device"),s=(e,t)=>e.filter((e=>e.area_id===t)),c=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),l=e=>e.sendMessagePromise({type:"config/device_registry/list"}),d=(e,t)=>e.subscribeEvents((0,r.D)((()=>l(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),h=(e,t)=>(0,n.B)("_dr",l,d,e,t)},5986:(e,t,i)=>{"use strict";i.d(t,{H0:()=>n,Lh:()=>o,F3:()=>r,t4:()=>a});const n=(e,t)=>t.issue_tracker||`https://github.com/home-assistant/home-assistant/issues?q=is%3Aissue+is%3Aopen+label%3A%22integration%3A+${e}%22`,o=(e,t)=>e(`component.${t}.title`)||t,r=e=>e.callWS({type:"manifest/list"}),a=(e,t)=>e.callWS({type:"manifest/get",integration:t})},91810:(e,t,i)=>{"use strict";i.d(t,{YJ:()=>n,ID:()=>o,Kk:()=>r,$c:()=>a,WI:()=>s,vY:()=>c,uZ:()=>l,cC:()=>d,e8:()=>h,Jl:()=>p,Lm:()=>u,ol:()=>f,x1:()=>m});const n=["ProtocolInfo","Probe","WakeUp","ManufacturerSpecific1","NodeInfo","NodePlusInfo","ManufacturerSpecific2","Versions","Instances","Static","CacheLoad","Associations","Neighbors","Session","Dynamic","Configuration","Complete"],o=["driverAllNodesQueried","driverAllNodesQueriedSomeDead","driverAwakeNodesQueried"],r=["starting","started","Ready","driverReady"],a=["Offline","stopped","driverFailed","driverReset","driverRemoved","driverAllNodesOnFire"],s=function(e){if(!e)return;const t=e.identifiers.find((e=>"ozw"===e[0]));if(!t)return;const i=t[1].split(".");return{node_id:parseInt(i[1]),ozw_instance:parseInt(i[0])}},c=e=>e.callWS({type:"ozw/get_instances"}),l=(e,t)=>e.callWS({type:"ozw/network_status",ozw_instance:t}),d=(e,t)=>e.callWS({type:"ozw/network_statistics",ozw_instance:t}),h=(e,t)=>e.callWS({type:"ozw/get_nodes",ozw_instance:t}),p=(e,t,i)=>e.callWS({type:"ozw/node_status",ozw_instance:t,node_id:i}),u=(e,t,i)=>e.callWS({type:"ozw/node_metadata",ozw_instance:t,node_id:i}),f=(e,t,i)=>e.callWS({type:"ozw/get_config_parameters",ozw_instance:t,node_id:i}),m=(e,t=!0)=>e.callWS({type:"ozw/migrate_zwave",dry_run:t})},60633:(e,t,i)=>{"use strict";i.d(t,{N8:()=>n,E0:()=>o,PH:()=>r,BM:()=>a,HV:()=>s,MI:()=>c,qc:()=>l,fQ:()=>d});const n=0,o=5,r=7,a=10,s=e=>e.callWS({type:"zwave/network_status"}),c=e=>e.callWS({type:"zwave/start_ozw_config_flow"}),l=e=>e.callWS({type:"zwave/get_migration_config"}),d=(e,t)=>e.callApi("GET",`zwave/config/${t}`)},2852:(e,t,i)=>{"use strict";i.d(t,{t:()=>l});var n=i(15652),o=i(85415),r=i(91177),a=i(73728),s=i(5986),c=i(52871);const l=(e,t)=>(0,c.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,a.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,i)=>(0,o.w)((0,s.Lh)(e.localize,t),(0,s.Lh)(e.localize,i))))},createFlow:async(e,t)=>{const[i]=await Promise.all([(0,a.Ky)(e,t),e.loadBackendTranslation("config",t)]);return i},fetchFlow:async(e,t)=>{const i=await(0,a.D4)(e,t);return await e.loadBackendTranslation("config",i.handler),i},handleFlowStep:a.XO,deleteFlow:a.oi,renderAbortDescription(e,t){const i=(0,r.I)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?n.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const i=(0,r.I)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?n.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${t.handler}.config.error.${i}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const i=(0,r.I)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return n.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=(0,r.I)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return n.dy`
        ${i?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const i=(0,r.I)(e.localize,`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?n.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""}})},52871:(e,t,i)=>{"use strict";i.d(t,{w:()=>r});var n=i(47181);const o=()=>Promise.all([i.e(5009),i.e(8161),i.e(2955),i.e(8200),i.e(879),i.e(9543),i.e(8374),i.e(2762),i.e(5829),i.e(1480),i.e(4421),i.e(8101),i.e(8331),i.e(4940),i.e(4482)]).then(i.bind(i,27234)),r=(e,t,i)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:o,dialogParams:{...t,flowConfig:i}})}},41896:(e,t,i)=>{"use strict";i.r(t),i.d(t,{ZwaveMigration:()=>k});i(53268),i(12730),i(53918),i(10983),i(31206);var n=i(15652),o=(i(60458),i(54909),i(22098),i(16509),i(60633)),r=i(11654),a=(i(88165),i(60010),i(2852)),s=i(91810),c=i(83849),l=i(26765),d=i(91741),h=i(57292),p=i(7323);function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var o=t.placement;if(t.kind===n&&("static"===o||"prototype"===o)){var r="static"===o?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!v(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:i,finishers:n};var r=this.decorateConstructor(i,t);return n.push.apply(n,r.finishers),r.finishers=n,r},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],o=e.decorators,r=o.length-1;r>=0;r--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[r])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var o=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[n])(o)||o);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=w(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:n,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function f(e){var t,i=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,n=new Array(t);i<t;i++)n[i]=e[i];return n}let k=function(e,t,i,n){var o=u();if(n)for(var r=0;r<n.length;r++)o=n[r](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},n=0;n<e.length;n++){var o,r=e[n];if("method"===r.kind&&(o=t.find(i)))if(g(r.descriptor)||g(o.descriptor)){if(v(r)||v(o))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");o.descriptor=r.descriptor}else{if(v(r)){if(v(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");o.decorators=r.decorators}m(r,o)}else t.push(r)}return t}(a.d.map(f)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("zwave-migration")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_networkStatus",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_step",value:()=>0},{kind:"field",decorators:[(0,n.sz)()],key:"_stoppingNetwork",value:()=>!1},{kind:"field",decorators:[(0,n.sz)()],key:"_migrationConfig",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_migrationData",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_migratedZwaveEntities",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_deviceNameLookup",value:()=>({})},{kind:"field",key:"_unsub",value:void 0},{kind:"field",key:"_unsubDevices",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){this._unsubscribe(),this._unsubDevices&&(this._unsubDevices(),this._unsubDevices=void 0)}},{kind:"method",key:"render",value:function(){return n.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/config/zwave"
      >
        <ha-config-section .narrow=${this.narrow} .isWide=${this.isWide}>
          <div slot="header">
            ${this.hass.localize("ui.panel.config.zwave.migration.ozw.header")}
          </div>

          <div slot="introduction">
            ${this.hass.localize("ui.panel.config.zwave.migration.ozw.introduction")}
          </div>
          ${(0,p.p)(this.hass,"hassio")||(0,p.p)(this.hass,"mqtt")?n.dy`
                ${0===this._step?n.dy`
                      <ha-card class="content" header="Introduction">
                        <div class="card-content">
                          <p>
                            This wizard will walk through the following steps to
                            migrate from the legacy Z-Wave integration to
                            OpenZWave.
                          </p>
                          <ol>
                            <li>Stop the Z-Wave network</li>
                            <li>
                              <i
                                >If running Home Assistant Core in Docker or in
                                Python venv:</i
                              >
                              Configure and start OZWDaemon
                            </li>
                            <li>Set up the OpenZWave integration</li>
                            <li>
                              Migrate entities and devices to the new
                              integration
                            </li>
                            <li>Remove legacy Z-Wave integration</li>
                          </ol>
                          <p>
                            <b>
                              Please take a backup or a snapshot of your
                              environment before proceeding.
                            </b>
                          </p>
                        </div>
                        <div class="card-actions">
                          <mwc-button @click=${this._continue}>
                            Continue
                          </mwc-button>
                        </div>
                      </ha-card>
                    `:""}
                ${1===this._step?n.dy`
                      <ha-card class="content" header="Stop Z-Wave Network">
                        <div class="card-content">
                          <p>
                            We need to stop the Z-Wave network to perform the
                            migration. Home Assistant will not be able to
                            control Z-Wave devices while the network is stopped.
                          </p>
                          ${this._stoppingNetwork?n.dy`
                                <div class="flex-container">
                                  <ha-circular-progress
                                    active
                                  ></ha-circular-progress>
                                  <div><p>Stopping Z-Wave Network...</p></div>
                                </div>
                              `:""}
                        </div>
                        <div class="card-actions">
                          <mwc-button @click=${this._stopNetwork}>
                            Stop Network
                          </mwc-button>
                        </div>
                      </ha-card>
                    `:""}
                ${2===this._step?n.dy`
                      <ha-card class="content" header="Set up OZWDaemon">
                        <div class="card-content">
                          <p>
                            Now it's time to set up the OZW integration.
                          </p>
                          ${(0,p.p)(this.hass,"hassio")?n.dy`
                                <p>
                                  The OZWDaemon runs in a Home Assistant addon
                                  that will be setup next. Make sure to check
                                  the checkbox for the addon.
                                </p>
                              `:n.dy`
                                <p>
                                  If you're using Home Assistant Core in Docker
                                  or a Python venv, see the
                                  <a
                                    href="https://github.com/OpenZWave/qt-openzwave/blob/master/README.md"
                                    target="_blank"
                                    rel="noreferrer"
                                  >
                                    OZWDaemon readme
                                  </a>
                                  for setup instructions.
                                </p>
                                <p>
                                  Here's the current Z-Wave configuration.
                                  You'll need these values when setting up OZW
                                  daemon.
                                </p>
                                ${this._migrationConfig?n.dy` <blockquote>
                                      USB Path:
                                      ${this._migrationConfig.usb_path}<br />
                                      Network Key:
                                      ${this._migrationConfig.network_key}
                                    </blockquote>`:""}
                                <p>
                                  Once OZWDaemon is installed, running, and
                                  connected to the MQTT broker click Continue to
                                  set up the OpenZWave integration and migrate
                                  your devices and entities.
                                </p>
                              `}
                        </div>
                        <div class="card-actions">
                          <mwc-button @click=${this._setupOzw}>
                            Continue
                          </mwc-button>
                        </div>
                      </ha-card>
                    `:""}
                ${3===this._step?n.dy`
                      <ha-card
                        class="content"
                        header="Migrate devices and entities"
                      >
                        <div class="card-content">
                          <p>
                            Now it's time to migrate your devices and entities
                            from the legacy Z-Wave integration to the OZW
                            integration, to make sure all your UI and
                            automations keep working.
                          </p>
                          ${this._migrationData?n.dy`
                                <p>Below is a list of what will be migrated.</p>
                                ${this._migratedZwaveEntities.length!==this._migrationData.zwave_entity_ids.length?n.dy`<h3 class="warning">
                                        Not all entities can be migrated! The
                                        following entities will not be migrated
                                        and might need manual adjustments to
                                        your config:
                                      </h3>
                                      <ul>
                                        ${this._migrationData.zwave_entity_ids.map((e=>this._migratedZwaveEntities.includes(e)?"":n.dy`<li>
                                                  ${(0,d.C)(this.hass.states[e])}
                                                  (${e})
                                                </li>`))}
                                      </ul>`:""}
                                ${Object.keys(this._migrationData.migration_device_map).length?n.dy`<h3>Devices that will be migrated:</h3>
                                      <ul>
                                        ${Object.keys(this._migrationData.migration_device_map).map((e=>n.dy`<li>
                                              ${this._deviceNameLookup[e]||e}
                                            </li>`))}
                                      </ul>`:""}
                                ${Object.keys(this._migrationData.migration_entity_map).length?n.dy`<h3>
                                        Entities that will be migrated:
                                      </h3>
                                      <ul>
                                        ${Object.keys(this._migrationData.migration_entity_map).map((e=>n.dy`<li>
                                            ${(0,d.C)(this.hass.states[e])}
                                            (${e})
                                          </li>`))}
                                      </ul>`:""}
                              `:n.dy` <div class="flex-container">
                                <p>Loading migration data...</p>
                                <ha-circular-progress active>
                                </ha-circular-progress>
                              </div>`}
                        </div>
                        <div class="card-actions">
                          <mwc-button @click=${this._doMigrate}>
                            Migrate
                          </mwc-button>
                        </div>
                      </ha-card>
                    `:""}
                ${4===this._step?n.dy`<ha-card class="content" header="Done!">
                      <div class="card-content">
                        That was all! You are now migrated to the new OZW
                        integration, check if all your devices and entities are
                        back the way they where, if not all entities could be
                        migrated you might have to change those manually.
                      </div>
                      <div class="card-actions">
                        <mwc-button @click=${this._navigateOzw}>
                          Go to OZW config panel
                        </mwc-button>
                      </div>
                    </ha-card>`:""}
              `:n.dy`
                <ha-card class="content" header="MQTT Required">
                  <div class="card-content">
                    <p>
                      OpenZWave requires MQTT. Please setup an MQTT broker and
                      the MQTT integration to proceed with the migration.
                    </p>
                  </div>
                </ha-card>
              `}
        </ha-config-section>
      </hass-subpage>
    `}},{kind:"method",key:"_getMigrationConfig",value:async function(){this._migrationConfig=await(0,o.qc)(this.hass)}},{kind:"method",key:"_unsubscribe",value:async function(){this._unsub&&((await this._unsub)(),this._unsub=void 0)}},{kind:"method",key:"_continue",value:function(){this._step++}},{kind:"method",key:"_stopNetwork",value:async function(){var e;this._stoppingNetwork=!0,await this._getNetworkStatus(),(null===(e=this._networkStatus)||void 0===e?void 0:e.state)!==o.N8?(this._unsub=this.hass.connection.subscribeEvents((()=>this._networkStopped()),"zwave.network_stop"),this.hass.callService("zwave","stop_network")):this._networkStopped()}},{kind:"method",key:"_setupOzw",value:async function(){var e;const t=await(0,o.MI)(this.hass);if((0,p.p)(this.hass,"ozw"))return this._getMigrationData(),void(this._step=3);(0,a.t)(this,{continueFlowId:t.flow_id,dialogClosedCallback:()=>{(0,p.p)(this.hass,"ozw")&&(this._getMigrationData(),this._step=3)},showAdvanced:null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced}),this.hass.loadBackendTranslation("title","ozw",!0)}},{kind:"method",key:"_getMigrationData",value:async function(){try{this._migrationData=await(0,s.x1)(this.hass,!0)}catch(e){return void(0,l.Ys)(this,{title:"Failed to get migration data!",text:"unknown_command"===e.code?"Restart Home Assistant and try again.":e.message})}this._migratedZwaveEntities=Object.keys(this._migrationData.migration_entity_map),Object.keys(this._migrationData.migration_device_map).length&&this._fetchDevices()}},{kind:"method",key:"_fetchDevices",value:function(){this._unsubDevices=(0,h.q4)(this.hass.connection,(e=>{if(!this._migrationData)return;const t=Object.keys(this._migrationData.migration_device_map),i={};e.forEach((e=>{t.includes(e.id)&&(i[e.id]=(0,h.jL)(e,this.hass))})),this._deviceNameLookup=i}))}},{kind:"method",key:"_doMigrate",value:async function(){(await(0,s.x1)(this.hass,!1)).migrated?this._step=4:(0,l.Ys)(this,{title:"Migration failed!"})}},{kind:"method",key:"_navigateOzw",value:function(){(0,c.c)(this,"/config/ozw")}},{kind:"method",key:"_networkStopped",value:function(){this._unsubscribe(),this._getMigrationConfig(),this._stoppingNetwork=!1,this._step=2}},{kind:"method",key:"_getNetworkStatus",value:async function(){this._networkStatus=await(0,o.HV)(this.hass)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.Qx,n.iv`
        .content {
          margin-top: 24px;
        }

        .flex-container {
          display: flex;
          align-items: center;
        }

        .flex-container ha-circular-progress {
          margin-right: 20px;
        }

        blockquote {
          display: block;
          background-color: var(--secondary-background-color);
          color: var(--primary-text-color);
          padding: 8px;
          margin: 8px 0;
          font-size: 0.9em;
          font-family: monospace;
        }

        ha-card {
          margin: 0 auto;
          max-width: 600px;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.530fab37cbe6c9b6d043.js.map