(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2211],{1090:(e,t,i)=>{"use strict";i(8878),i(30879),i(53973),i(51095);var n=i(50856),a=i(28426);class r extends a.H3{static get template(){return n.d`
      <style>
        :host {
          display: block;
          @apply --paper-font-common-base;
        }

        paper-input {
          width: 30px;
          text-align: center;
          --paper-input-container-input: {
            /* Damn you firefox
             * Needed to hide spin num in firefox
             * http://stackoverflow.com/questions/3790935/can-i-hide-the-html5-number-input-s-spin-box
             */
            -moz-appearance: textfield;
            @apply --paper-time-input-cotnainer;
          }
          --paper-input-container-input-webkit-spinner: {
            -webkit-appearance: none;
            margin: 0;
            display: none;
          }
          --paper-input-container-shared-input-style_-_-webkit-appearance: textfield;
        }

        paper-dropdown-menu {
          width: 55px;
          padding: 0;
          /* Force ripple to use the whole container */
          --paper-dropdown-menu-ripple: {
            color: var(
              --paper-time-input-dropdown-ripple-color,
              var(--primary-color)
            );
          }
          --paper-input-container-input: {
            @apply --paper-font-button;
            text-align: center;
            padding-left: 5px;
            @apply --paper-time-dropdown-input-cotnainer;
          }
          --paper-input-container-underline: {
            border-color: transparent;
          }
          --paper-input-container-underline-focus: {
            border-color: transparent;
          }
        }

        paper-item {
          cursor: pointer;
          text-align: center;
          font-size: 14px;
        }

        paper-listbox {
          padding: 0;
        }

        label {
          @apply --paper-font-caption;
          color: var(
            --paper-input-container-color,
            var(--secondary-text-color)
          );
        }

        .time-input-wrap {
          @apply --layout-horizontal;
          @apply --layout-no-wrap;
          justify-content: var(--paper-time-input-justify-content, normal);
        }

        [hidden] {
          display: none !important;
        }

        #millisec {
          width: 38px;
        }
      </style>

      <label hidden$="[[hideLabel]]">[[label]]</label>
      <div class="time-input-wrap">
        <!-- Hour Input -->
        <paper-input
          id="hour"
          type="number"
          value="{{hour}}"
          label="[[hourLabel]]"
          on-change="_shouldFormatHour"
          on-focus="_onFocus"
          required
          prevent-invalid-input
          auto-validate="[[autoValidate]]"
          maxlength="2"
          max="[[_computeHourMax(format)]]"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
        >
          <span suffix="" slot="suffix">:</span>
        </paper-input>

        <!-- Min Input -->
        <paper-input
          id="min"
          type="number"
          value="{{min}}"
          label="[[minLabel]]"
          on-change="_formatMin"
          on-focus="_onFocus"
          required
          auto-validate="[[autoValidate]]"
          prevent-invalid-input
          maxlength="2"
          max="59"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
        >
          <span hidden$="[[!enableSecond]]" suffix slot="suffix">:</span>
        </paper-input>

        <!-- Sec Input -->
        <paper-input
          id="sec"
          type="number"
          value="{{sec}}"
          label="[[secLabel]]"
          on-change="_formatSec"
          on-focus="_onFocus"
          required
          auto-validate="[[autoValidate]]"
          prevent-invalid-input
          maxlength="2"
          max="59"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
          hidden$="[[!enableSecond]]"
        >
          <span hidden$="[[!enableMillisecond]]" suffix slot="suffix">:</span>
        </paper-input>

        <!-- Millisec Input -->
        <paper-input
          id="millisec"
          type="number"
          value="{{millisec}}"
          label="[[millisecLabel]]"
          on-change="_formatMillisec"
          on-focus="_onFocus"
          required
          auto-validate="[[autoValidate]]"
          prevent-invalid-input
          maxlength="3"
          max="999"
          min="0"
          no-label-float$="[[!floatInputLabels]]"
          always-float-label$="[[alwaysFloatInputLabels]]"
          disabled="[[disabled]]"
          hidden$="[[!enableMillisecond]]"
        >
        </paper-input>

        <!-- Dropdown Menu -->
        <paper-dropdown-menu
          id="dropdown"
          required=""
          hidden$="[[_equal(format, 24)]]"
          no-label-float=""
          disabled="[[disabled]]"
        >
          <paper-listbox
            attr-for-selected="name"
            selected="{{amPm}}"
            slot="dropdown-content"
          >
            <paper-item name="AM">AM</paper-item>
            <paper-item name="PM">PM</paper-item>
          </paper-listbox>
        </paper-dropdown-menu>
      </div>
    `}static get properties(){return{label:{type:String,value:"Time"},autoValidate:{type:Boolean,value:!0},hideLabel:{type:Boolean,value:!1},floatInputLabels:{type:Boolean,value:!1},alwaysFloatInputLabels:{type:Boolean,value:!1},format:{type:Number,value:12},disabled:{type:Boolean,value:!1},hour:{type:String,notify:!0},min:{type:String,notify:!0},sec:{type:String,notify:!0},millisec:{type:String,notify:!0},hourLabel:{type:String,value:""},minLabel:{type:String,value:":"},secLabel:{type:String,value:""},millisecLabel:{type:String,value:""},enableSecond:{type:Boolean,value:!1},enableMillisecond:{type:Boolean,value:!1},noHoursLimit:{type:Boolean,value:!1},amPm:{type:String,notify:!0,value:"AM"},value:{type:String,notify:!0,readOnly:!0,computed:"_computeTime(min, hour, sec, millisec, amPm)"}}}validate(){let e=!0;return this.$.hour.validate()&&this.$.min.validate()||(e=!1),this.enableSecond&&!this.$.sec.validate()&&(e=!1),this.enableMillisecond&&!this.$.millisec.validate()&&(e=!1),12!==this.format||this.$.dropdown.validate()||(e=!1),e}_computeTime(e,t,i,n,a){let r;return(t||e||i&&this.enableSecond||n&&this.enableMillisecond)&&(i=i||"00",n=n||"000",r=(t=t||"00")+":"+(e=e||"00"),this.enableSecond&&i&&(r=r+":"+i),this.enableMillisecond&&n&&(r=r+":"+n),12===this.format&&(r=r+" "+a)),r}_onFocus(e){e.target.inputElement.inputElement.select()}_formatMillisec(){1===this.millisec.toString().length&&(this.millisec=this.millisec.toString().padStart(3,"0"))}_formatSec(){1===this.sec.toString().length&&(this.sec=this.sec.toString().padStart(2,"0"))}_formatMin(){1===this.min.toString().length&&(this.min=this.min.toString().padStart(2,"0"))}_shouldFormatHour(){24===this.format&&1===this.hour.toString().length&&(this.hour=this.hour.toString().padStart(2,"0"))}_computeHourMax(e){return this.noHoursLimit?null:12===e?e:23}_equal(e,t){return e===t}}customElements.define("paper-time-input",r)},9535:(e,t,i)=>{"use strict";i.r(t);i(53268),i(12730);var n=i(15652),a=(i(60010),i(38353),i(63081),i(47181)),r=(i(1090),i(81545),i(81689),i(94469)),o=i(11654);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var a=t.placement;if(t.kind===n&&("static"===a||"prototype"===a)){var r="static"===a?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:i,finishers:n};var r=this.decorateConstructor(i,t);return n.push.apply(n,r.finishers),r.finishers=n,r},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],a=e.decorators,r=a.length-1;r>=0;r--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[r])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var p=0;p<c.length;p++)this.addElementPlacement(c[p],t);i.push.apply(i,c)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var a=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[n])(a)||a);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:n,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,n=new Array(t);i<t;i++)n[i]=e[i];return n}!function(e,t,i,n){var a=s();if(n)for(var r=0;r<n.length;r++)a=n[r](a);var o=t((function(e){a.initializeInstanceElements(e,u.elements)}),i),u=a.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},n=0;n<e.length;n++){var a,r=e[n];if("method"===r.kind&&(a=t.find(i)))if(d(r.descriptor)||d(a.descriptor)){if(p(r)||p(a))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");a.descriptor=r.descriptor}else{if(p(r)){if(p(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");a.decorators=r.decorators}c(r,a)}else t.push(r)}return t}(o.d.map(l)),e);a.initializeClassElements(o.F,u.elements),a.runClassFinishers(o.F,u.finishers)}([(0,n.Mo)("ha-config-ais-dom-config-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"selectedVoice",value:()=>""},{kind:"method",key:"firstUpdated",value:function(){this.selectedVoice=this.hass.states["input_select.assistant_voice"].state}},{kind:"method",key:"render",value:function(){return n.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <!-- <ha-button-menu corner="BOTTOM_START" slot="toolbar-icon">
            <ha-icon-button
              icon="hass:dots-vertical"
              label="Menu"
              slot="trigger"
            >
            </ha-icon-button>
            <mwc-list-item>
                Edit ais_welcome.txt
            </mwc-list-item>
        </ha-button-menu> -->
        <div .narrow=${this.narrow}>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Ustawienia głosu Asystenta</span>
            <span slot="introduction"
              >Możesz zmienić głos asystenta i dostosować szybkość i ton mowy
              oraz komunikat mówiony przez asystenta podczas startu
              systemu..</span
            >
            <ha-card header="Wybór głosu Asystenta">
              <div class="card-content">
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Jola online")}
                    data-voice="Jola online"
                    alt="Jola Online"
                    title="Jola Online"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Ania.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Jola lokalnie")}
                    data-voice="Jola lokalnie"
                    alt="Jola Lokalnie"
                    title="Jola Lokalnie"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Asia.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Celina")}
                    data-voice="Celina"
                    alt="Celina"
                    title="Celina"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Celka.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Anżela")}
                    data-voice="Anżela"
                    alt="Anżela"
                    title="Anżela"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Anzela.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Asia")}
                    data-voice="Asia"
                    alt="Asia"
                    title="Asia"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Kasia.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Sebastian")}
                    data-voice="Sebastian"
                    alt="Sebastian"
                    title="Sebastian"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Sebastian.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Bartek")}
                    data-voice="Bartek"
                    alt="Bartek"
                    title="Bartek"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Bartek.jpg"
                  />
                </div>
                <div class="person">
                  <img
                    class=${this.personImgClass(this.selectedVoice,"Andrzej")}
                    data-voice="Andrzej"
                    alt="Andrzej"
                    title="Andrzej"
                    @click=${this.switchTtsPerson}
                    src="/static/ais_dom/Andrzej.jpg"
                  />
                </div>
              </div>
              <div class="card-actions person-actions">
                <div @click=${this.tuneVoiceTone}>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:tune"
                  ></ha-icon-button
                  ><mwc-button>Ton mowy</mwc-button>
                </div>
                <div @click=${this.tuneVoiceSpeed}>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:play-speed"
                  ></ha-icon-button
                  ><mwc-button>Szybkość mowy</mwc-button>
                </div>
                <div @click=${this._openAisWelcomeText}>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:file-document-edit-outline"
                  ></ha-icon-button
                  ><mwc-button>Welcome.txt</mwc-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,n.iv`
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .card-actions {
          display: flex;
        }
        ha-card > paper-toggle-button {
          margin: -4px 0;
          position: absolute;
          top: 32px;
          right: 8px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        div.person {
          display: inline-block;
          margin: 10px;
        }
        img {
          border-radius: 50%;
          width: 100px;
          height: 100px;
          border: 20px;
        }
        img.person-img-selected {
          border: 7px solid var(--primary-color);
          width: 110px;
          height: 110px;
        }
      `]}},{kind:"method",key:"_openAisWelcomeText",value:async function(){const e="/data/data/pl.sviete.dom/files/home/AIS/ais_welcome.txt",t={dialogTitle:"Edit ais_welcome.txt",filePath:e,fileBody:await this.hass.callApi("POST","ais_file/read",{filePath:e}),readonly:!1};(0,r.j)(this,t)}},{kind:"method",key:"computeClasses",value:function(e){return e?"content":"content narrow"}},{kind:"method",key:"personImgClass",value:function(e,t){return e===t?"person-img-selected":""}},{kind:"method",key:"tuneVoiceSpeed",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"input_number.assistant_rate"})}},{kind:"method",key:"tuneVoiceTone",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"input_number.assistant_tone"})}},{kind:"method",key:"switchTtsPerson",value:function(e){this.selectedVoice=e.target.dataset.voice,this.hass.callService("input_select","select_option",{entity_id:"input_select.assistant_voice",option:e.target.dataset.voice})}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.d786edd9762a0f1732f8.js.map