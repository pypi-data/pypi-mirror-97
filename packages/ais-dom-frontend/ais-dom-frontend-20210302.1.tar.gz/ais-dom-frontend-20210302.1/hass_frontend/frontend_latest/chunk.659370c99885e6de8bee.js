/*! For license information please see chunk.659370c99885e6de8bee.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6329,1203],{8878:(e,t,i)=>{"use strict";i(43437),i(8621),i(63207),i(30879),i(78814),i(60748),i(57548),i(73962);var r=i(51644),n=i(26110),o=i(21006),a=i(98235),s=i(9672),l=i(87156),d=i(81668),c=i(50856);(0,s.k)({_template:c.d`
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
`,is:"paper-dropdown-menu",behaviors:[r.P,n.a,o.V,a.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,l.vz)(this.$.content).getDistributedNodes(),t=0,i=e.length;t<i;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){d.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},49706:(e,t,i)=>{"use strict";i.d(t,{Rb:()=>r,Zy:()=>n,h2:()=>o,PS:()=>a,l:()=>s,ht:()=>l,f0:()=>d,tj:()=>c,uo:()=>p,lC:()=>u,Kk:()=>h,iY:()=>m,ot:()=>f,gD:()=>y,a1:()=>b,AZ:()=>g});const r="hass:bookmark",n={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",number:"hass:ray-vertex",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},o={current:"hass:current-ac",energy:"hass:flash",humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",power_factor:"hass:angle-acute",signal_strength:"hass:wifi",timestamp:"hass:clock",voltage:"hass:sine-wave"},a=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","number","scene","script","timer","vacuum","water_heater"],s=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","number","scene"],d=["camera","configurator","scene"],c=["closed","locked","off"],p="on",u="off",h=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),m=new Set(["camera","media_player"]),f="°C",y="°F",b="group.default_view",g=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"]},91168:(e,t,i)=>{"use strict";i.d(t,{Z:()=>n});const r=e=>e<10?`0${e}`:e;function n(e){const t=Math.floor(e/3600),i=Math.floor(e%3600/60),n=Math.floor(e%3600%60);return t>0?`${t}:${r(i)}:${r(n)}`:i>0?`${i}:${r(n)}`:n>0?""+n:null}},22311:(e,t,i)=>{"use strict";i.d(t,{N:()=>n});var r=i(58831);const n=e=>(0,r.M)(e.entity_id)},83599:(e,t,i)=>{"use strict";i.d(t,{m:()=>r});const r=e=>{if(!e.attributes.remaining)return;let t=function(e){const t=e.split(":").map(Number);return 3600*t[0]+60*t[1]+t[2]}(e.attributes.remaining);if("active"===e.state){const i=(new Date).getTime(),r=new Date(e.last_changed).getTime();t=Math.max(t-(i-r)/1e3,0)}return t}},81303:(e,t,i)=>{"use strict";i(8878);const r=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends r{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},43408:(e,t,i)=>{"use strict";i.d(t,{H:()=>r});const r=e=>e.callWS({type:"webhook/list"})},26765:(e,t,i)=>{"use strict";i.d(t,{Ys:()=>a,g7:()=>s,D9:()=>l});var r=i(47181);const n=()=>Promise.all([i.e(8200),i.e(879),i.e(2762),i.e(8345),i.e(6509),i.e(32)]).then(i.bind(i,1281)),o=(e,t,i)=>new Promise((o=>{const a=t.cancel,s=t.confirm;(0,r.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:n,dialogParams:{...t,...i,cancel:()=>{o(!!(null==i?void 0:i.prompt)&&null),a&&a()},confirm:e=>{o(!(null==i?void 0:i.prompt)||e),s&&s(e)}}})})),a=(e,t)=>o(e,t),s=(e,t)=>o(e,t,{confirmation:!0}),l=(e,t)=>o(e,t,{prompt:!0})},6942:(e,t,i)=>{"use strict";i.r(t);i(53268),i(12730);var r=i(50856),n=i(28426);i(60010),i(38353),i(63081),i(81303),i(43709),i(8878),i(53973),i(51095),i(54909),i(16509);class o extends n.H3{static get template(){return r.d`
      <style include="iron-flex ha-style">
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
        ha-card > div#card-icon {
          margin: -4px 0;
          position: absolute;
          top: 1em;
          right: 1em;
          border-radius: 25px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        .config-invalid .text {
          color: var(--google-red-500);
          font-weight: 500;
        }

        @keyframes pulse {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: var(--primary-color);
          }
        }
        @keyframes pulseRed {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: var(--material-error-color);
          }
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienie zapisu logów systemu</span>
            <span slot="introduction"
              >Tu możesz skonfigurować zapis logów do pliku na wymiennym
              dysku</span
            >
            <ha-card header="Zapis logów systemu do pliku">
              <div id="card-icon" style$="[[logIconAnimationStyle]]">
                <ha-icon-button icon="mdi:record-rec"></ha-icon-button>
              </div>
              <div class="card-content">
                Żeby włączyć logowanie w systemie Asystent domowy, wystarczy
                wybrać lokalizację na dysku wymiennym, w której będzie
                zapisywany plik z rejestrem działań w systemie. <br />
                Dodatkowo można też określić poziom szczegółowości logowania i
                liczbę dni przechowywanych w jednym pliku loga. <br /><br />
                Wybór dysku do zapisu logów systemu: <br />
                <ha-icon-button icon="mdi:usb-flash-drive"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Wybrany dysk"
                  dynamic-align=""
                  label="Dyski wymienne"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[logDrive]]"
                    on-selected-changed="logDriveChanged"
                    attr-for-selected="item-name"
                  >
                    <template
                      is="dom-repeat"
                      items="[[usbDrives.attributes.options]]"
                    >
                      <paper-item item-name$="[[item]]">[[item]]</paper-item>
                    </template>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
              </div>
              <div class="card-content">
                Wybór poziomu logowania: <br />
                <ha-icon-button icon="mdi:bug-check"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Poziom logowania"
                  dynamic-align=""
                  label="Poziomy logowania"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[logLevel]]"
                    on-selected-changed="logLevelChanged"
                    attr-for-selected="item-name"
                  >
                    <paper-item item-name="critical">critical</paper-item>
                    <paper-item item-name="fatal">fatal</paper-item>
                    <paper-item item-name="error">error</paper-item>
                    <paper-item item-name="warning">warning</paper-item>
                    <paper-item item-name="warn">warn</paper-item>
                    <paper-item item-name="info">info</paper-item>
                    <paper-item item-name="debug">debug</paper-item>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
                <br /><br />
                W tym miejscu możesz określić liczbę dni przechowywanych w
                jednym pliku loga. Rotacja plików dziennika wykonywna jest o
                północy.
                <paper-input
                  type="number"
                  value="[[logRotating]]"
                  on-change="logRotatingDaysChanged"
                  maxlength="4"
                  max="9999"
                  min="1"
                  label-float="Liczba dni przechowywanych w jednym pliku loga"
                  label="Liczba dni przechowywanych w jednym pliku loga"
                >
                  <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                </paper-input>
                <div class="config-invalid">
                  <span class="text">
                    [[logError]]
                  </span>
                </div>
              </div>
              <div class="card-content">
                [[logModeInfo]]
              </div>
              <div class="card-content">
                * Zmiana poziomu logowania wykonywana jest online - po tej
                zmianie nie trzeba ponownie uruchomieć systemu. Zastosowanie
                zmiany dysku do zapisu systemu lub zmiany liczby dni
                przechowywanych w jednym pliku loga wymaga restartu systemu.
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia zapisu zdarzeń systemu</span>
            <span slot="introduction">
              Tu możesz skonfigurować zapis zdarzeń do bazy danych na dysku
              wymiennym lub do zdalnego serwera bazodanowego
            </span>
            <ha-card header="Zapis zdarzeń do bazy danych">
              <div id="card-icon" style$="[[dbIconAnimationStyle]]">
                <ha-icon-button icon="mdi:database"></ha-icon-button>
              </div>
              <div class="card-content">
                Wybierz silnik bazodanowy, który chcesz użyć do rejestracji
                zdarzeń.<br /><br />Najprostszy wybór to baza SQLite, która nie
                wymaga konfiguracji i może rejestrować dane w pamięci - taka
                baza jest automatycznie używana, gdy rejestracja zdarzeń
                włączana jest przez integrację (np. Historia lub Dziennik).
                <br /><br />Gdy system generuje więcej zdarzeń lub gdy chcesz
                mieć dostęp do historii, to zalecamy zapisywać zdarzenia na
                zewnętrznym dysku lub w zdalnej bazie danych. <br /><br />
                Wybór silnika bazy danych:
                <br />
                <ha-icon-button icon="mdi:database"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Silnik bazy danych"
                  dynamic-align=""
                  label="Silnik bazy danych"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[dbEngine]]"
                    on-selected-changed="dbEngineChanged"
                    attr-for-selected="item-name"
                  >
                    <paper-item item-name="-">-</paper-item>
                    <paper-item item-name="SQLite (memory)"
                      >SQLite (memory)</paper-item
                    >
                    <paper-item item-name="SQLite (file)"
                      >SQLite (file)</paper-item
                    >
                    <paper-item item-name="MariaDB">MariaDB</paper-item>
                    <paper-item item-name="MySQL">MySQL</paper-item>
                    <paper-item item-name="PostgreSQL">PostgreSQL</paper-item>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
              </div>
              <div class="card-content" style$="[[dbFileDisplayStyle]]">
                Wybór dysku do zapisu bazy danych: <br />
                <ha-icon-button icon="mdi:usb-flash-drive"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Wybrany dysk"
                  dynamic-align=""
                  label="Dyski wymienne"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[dbDrive]]"
                    on-selected-changed="dbDriveChanged"
                    attr-for-selected="item-name"
                  >
                    <template
                      is="dom-repeat"
                      items="[[usbDrives.attributes.options]]"
                    >
                      <paper-item item-name$="[[item]]">[[item]]</paper-item>
                    </template>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
                <br /><br />
              </div>
              <div class="card-content" style$="[[dbConectionDisplayStyle]]">
                Parametry połączenia z bazą danych: <br />
                <paper-input
                  placeholder="Użytkownik"
                  type="text"
                  id="db_user"
                  value="[[dbUser]]"
                  on-change="_computeDbUrl"
                >
                  <ha-icon icon="mdi:account" slot="suffix"></ha-icon>
                </paper-input>
                <paper-input
                  placeholder="Hasło"
                  no-label-float=""
                  type="password"
                  id="db_password"
                  value="[[dbPassword]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:lastpass" slot="suffix"></ha-icon
                ></paper-input>
                <paper-input
                  placeholder="IP Serwera DB"
                  no-label-float=""
                  type="text"
                  id="db_server_ip"
                  value="[[dbServerIp]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:ip-network" slot="suffix"></ha-icon
                ></paper-input>
                <paper-input
                  placeholder="Nazwa bazy"
                  no-label-float=""
                  type="text"
                  id="db_server_name"
                  value="[[dbServerName]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:database-check" slot="suffix"></ha-icon
                ></paper-input>
                <br /><br />
              </div>
              <div class="card-content" style$="[[dbKeepDaysDisplayStyle]]">
                Żeby utrzymać system w dobrej kondycji, codziennie dokładnie o
                godzinie 4:12 rano Asystent usuwa z bazy zdarzenia i stany
                starsze niż <b>określona liczba dni</b> (2 dni dla bazy w
                pamięci urządzenia i domyślnie 10 dla innych lokalizacji).
                <br />
                W tym miejscu możesz określić liczbę dni, których historia ma
                być przechowywana w bazie danych.
                <paper-input
                  id="db_keep_days"
                  type="number"
                  value="[[dbKeepDays]]"
                  on-change="_computeDbUrl"
                  maxlength="4"
                  max="9999"
                  min="1"
                  label-float="Liczba dni historii przechowywanych w bazie"
                  label="Liczba dni historii przechowywanych w bazie"
                >
                  <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                </paper-input>
              </div>
              <div class="card-content">
                [[dbUrl]]
                <br /><br />
                <div class="center-container">
                  <template is="dom-if" if="[[dbConnectionValidating]]">
                    <paper-spinner active=""></paper-spinner>
                  </template>
                  <template is="dom-if" if="[[!dbConnectionValidating]]">
                    <div class="config-invalid">
                      <span class="text">
                        [[validationError]]
                      </span>
                    </div>
                    <ha-call-service-button
                      class="warning"
                      hass="[[hass]]"
                      domain="ais_files"
                      service="check_db_connection"
                      service-data="[[_addAisDbConnectionData()]]"
                      >[[dbConnectionInfoButton]]
                    </ha-call-service-button>
                  </template>
                </div>
                <div>
                  * po zmianie połączenia z bazą wymagany jest restart systemu.
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,logLevel:{type:String,value:"info"},logDrive:{type:String,value:"-"},logError:{type:String,computed:"_computeLogsSettings(hass)"},logRotating:Number,logIconAnimationStyle:String,dbIconAnimationStyle:String,usbDrives:{type:Object,computed:"_computeUsbDrives(hass)"},dbDrives:{type:Object,computed:"_computeDbDrives(hass)"},dbConnectionValidating:{type:Boolean,value:!1},dbConnectionInfoButton:{type:String,computed:"_computeDbConnectionSettings(hass)"},validationError:String,logModeInfo:String,dbUrl:String,dbConectionDisplayStyle:String,dbFileDisplayStyle:String,dbKeepDaysDisplayStyle:String,dbDrive:String,dbEngine:String,dbUser:String,dbPassword:String,dbServerIp:String,dbServerName:String,dbKeepDays:Number}}ready(){super.ready(),this.hass.callService("ais_files","get_db_log_settings_info"),this._computeLogsSettings(this.hass)}computeClasses(e){return e?"content":"content narrow"}_computeUsbDrives(e){return e.states["input_select.ais_usb_flash_drives"]}_computeLogsSettings(e){const t=e.states["sensor.ais_logs_settings_info"],i=t.attributes;this.logDrive=i.logDrive,this.logLevel=i.logLevel,this.logRotating=i.logRotating,t.state>0?"debug"===this.logLevel?this.logIconAnimationStyle="animation: pulseRed 2s infinite;":"info"===this.logLevel?this.logIconAnimationStyle="animation: pulseRed 4s infinite;":"info"===this.logLevel?this.logIconAnimationStyle="animation: pulse 5s infinite;":"warn"===this.logLevel?this.logIconAnimationStyle="animation: pulse 6s infinite;":"warning"===this.logLevel?this.logIconAnimationStyle="animation: pulse 7s infinite;":"error"===this.logLevel?this.logIconAnimationStyle="animation: pulse 8s infinite;":"fatal"===this.logLevel?this.logIconAnimationStyle="animation: pulse 9s infinite;":"critical"===this.logLevel&&(this.logIconAnimationStyle="animation: pulse 10s infinite;"):this.logIconAnimationStyle="";let r="";return i.logError&&(r=i.logError),"debug"===this.logLevel&&t.state&&(r+=" Logowanie w trybie debug generuje duże ilości logów i obciąża system. Używaj go tylko na czas diagnozowania problemu. "),r}logDriveChanged(e){this.logDrive=e.detail.value,"-"!==this.logDrive?this.logModeInfo="Zapis logów do pliku /dyski-wymienne/"+this.logDrive+"/ais.log":this.logModeInfo="Zapis logów do pliku wyłączony ",this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}logLevelChanged(e){this.logLevel=e.detail.value,this.logModeInfo="Poziom logów: "+this.logLevel,this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}logRotatingDaysChanged(e){this.logRotating=Number(e.target.value),1===this.logRotating?this.logModeInfo="Rotacja logów codziennie.":this.logModeInfo="Rotacja logów co "+this.logRotating+" dni.",this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}_computeDbConnectionSettings(e){const t=e.states["sensor.ais_db_connection_info"],i=t.attributes;this.validationError=i.errorInfo,this.dbEngine=i.dbEngine,this.dbEngine||(this.dbEngine="-"),this.dbDrive||(this.dbDrive=i.dbDrive),this.dbUrl=i.dbUrl,this.dbPassword=i.dbPassword,this.dbUser=i.dbUser,this.dbServerIp=i.dbServerIp,this.dbServerName=i.dbServerName,this.dbKeepDays=i.dbKeepDays;let r="";return"no_db_url_saved"===t.state?(r="Sprawdź połączenie",this.dbIconAnimationStyle=""):"db_url_saved"===t.state?(r="Usuń polączenie",this.dbIconAnimationStyle="animation: pulse 6s infinite;"):"db_url_not_valid"===t.state?(r="Sprawdź połączenie",this.dbIconAnimationStyle="animation: pulseRed 3s infinite;"):"db_url_valid"===t.state&&(r="Zapisz połączenie",this.dbIconAnimationStyle="animation: pulse 4s infinite;"),this.dbConnectionValidating=!1,this._doComputeDbUrl(!1),r}_addAisDbConnectionData(){return{buttonClick:!0}}_computeDbDrives(e){return e.states["input_select.ais_usb_flash_drives"]}_doComputeDbUrl(e){let t="";if("-"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="display: none",this.dbKeepDaysDisplayStyle="display: none",t="";else if("SQLite (file)"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="",this.dbKeepDaysDisplayStyle="",t="sqlite://///data/data/pl.sviete.dom/files/home/dom/dyski-wymienne/"+this.dbDrive+"/ais.db",e&&(this.dbKeepDays=this.shadowRoot.getElementById("db_keep_days").value);else if("SQLite (memory)"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="display: none",this.dbKeepDaysDisplayStyle="display: none",t="sqlite:///:memory:";else{this.dbFileDisplayStyle="display: none",this.dbConectionDisplayStyle="",this.dbKeepDaysDisplayStyle="",e&&(this.dbPassword=this.shadowRoot.getElementById("db_password").value,this.dbUser=this.shadowRoot.getElementById("db_user").value,this.dbServerIp=this.shadowRoot.getElementById("db_server_ip").value,this.dbServerName=this.shadowRoot.getElementById("db_server_name").value,this.dbKeepDays=this.shadowRoot.getElementById("db_keep_days").value);let i="";(this.dbUser||this.dbPassword)&&(i=this.dbUser+":"+this.dbPassword+"@"),"MariaDB"===this.dbEngine?t="mysql+pymysql://"+i+this.dbServerIp+"/"+this.dbServerName+"?charset=utf8mb4":"MySQL"===this.dbEngine?t="mysql://"+i+this.dbServerIp+"/"+this.dbServerName+"?charset=utf8mb4":"PostgreSQL"===this.dbEngine&&(t="postgresql://"+i+this.dbServerIp+"/"+this.dbServerName)}this.dbUrl=t}_computeDbUrl(){this._doComputeDbUrl(!0),this.hass.callService("ais_files","check_db_connection",{buttonClick:!1,dbEngine:this.dbEngine,dbDrive:this.dbDrive,dbUrl:this.dbUrl,dbPassword:this.dbPassword,dbUser:this.dbUser,dbServerIp:this.dbServerIp,dbServerName:this.dbServerName,dbKeepDays:this.dbKeepDays,errorInfo:""})}dbDriveChanged(e){const t=e.detail.value;this.dbDrive=t,this._computeDbUrl()}dbEngineChanged(e){const t=e.detail.value;this.dbEngine=t,this._computeDbUrl()}}customElements.define("ha-config-ais-dom-config-logs",o)},96326:(e,t,i)=>{"use strict";i.r(t);i(31203),i(53268),i(12730);var r=i(15652),n=(i(60010),i(38353),i(63081),i(53973),i(89194),i(22098),i(43408)),o=i(47181);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function s(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let y=function(e,t,i,r){var n=a();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var p=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(c(o.descriptor)||c(n.descriptor)){if(d(o)||d(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(d(o)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(p.d.map(s)),e);return n.initializeClassElements(p.F,u.elements),n.runClassFinishers(p.F,u.finishers)}(null,(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"_localHooks",value:void 0},{kind:"get",static:!0,key:"properties",value:function(){return{hass:{},_localHooks:{}}}},{kind:"method",key:"connectedCallback",value:function(){m(f(a.prototype),"connectedCallback",this).call(this),this._fetchData()}},{kind:"method",key:"render",value:function(){return r.dy`
      ${this.renderStyle()}
      <ha-card header="Wywołania zwrotne HTTP">
        <div class="card-content">
          Wywołania zwrotne HTTP (Webhook) używane są do udostępniania
          powiadomień o zdarzeniach. Wszystko, co jest skonfigurowane do
          uruchamiania przez wywołanie zwrotne, ma publicznie dostępny unikalny
          adres URL, aby umożliwić wysyłanie danych do Asystenta domowego z
          dowolnego miejsca. ${this._renderBody()}

          <div class="footer">
            <a href="https://www.ai-speaker.com/" target="_blank">
              Dowiedz się więcej o zwrotnym wywołaniu HTTP.
            </a>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_renderBody",value:function(){return this._localHooks?1===this._localHooks.length?r.dy`
        <div class="body-text">
          Wygląda na to, że nie masz jeszcze zdefiniowanych żadnych wywołań
          zwrotnych. Rozpocznij od skonfigurowania
          <a href="/config/integrations">
            integracji opartej na wywołaniu zwrotnym
          </a>
          lub przez tworzenie
          <a href="/config/automation/new"> automatyzacji typu webhook </a>.
        </div>
      `:this._localHooks.map((e=>r.dy`
        ${"aisdomprocesscommandfromframe"===e.webhook_id?r.dy` <div></div> `:r.dy`
              <div class="webhook" .entry="${e}">
                <paper-item-body two-line>
                  <div>
                    ${e.name}
                    ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
                  </div>
                  <div secondary>${e.webhook_id}</div>
                </paper-item-body>
                <mwc-button @click="${this._handleManageButton}">
                  Pokaż
                </mwc-button>
              </div>
            `}
      `)):r.dy` <div class="body-text">Pobieranie…</div> `}},{kind:"method",key:"_showDialog",value:function(e){const t=this._localHooks.find((t=>t.webhook_id===e));var r,n;r=this,n={webhook:t},(0,o.B)(r,"show-dialog",{dialogTag:"dialog-manage-ais-cloudhook",dialogImport:()=>i.e(4795).then(i.bind(i,96519)),dialogParams:n})}},{kind:"method",key:"_handleManageButton",value:function(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}},{kind:"method",key:"_fetchData",value:async function(){this._localHooks=await(0,n.H)(this.hass)}},{kind:"method",key:"renderStyle",value:function(){return r.dy`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}}]}}),r.oi);customElements.define("ais-webhooks",y);i(43709);function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!w(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return E(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?E(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=z(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function g(e){var t,i=z(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function z(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function E(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=b();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(k(o.descriptor)||k(n.descriptor)){if(w(o)||w(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(w(o)){if(w(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}v(o,n)}else t.push(o)}return t}(a.d.map(g)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,r.Mo)("ha-config-ais-dom-config-remote")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_qrCode",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"remoteDomain",value:void 0},{kind:"method",key:"_generateQR",value:async function(){const e=await Promise.all([i.e(9033),i.e(1970)]).then(i.t.bind(i,51970,19)),t=await e.toCanvas(`${this.remoteDomain}`,{width:280,errorCorrectionLevel:"Q"}),n=t.getContext("2d"),o=new Image;o.src="/static/icons/favicon-192x192.png",await new Promise((e=>{o.onload=e})),n.drawImage(o,t.width/3,t.height/3,t.width/3,t.height/3),this._qrCode=r.dy`<img src=${t.toDataURL()}></img>`}},{kind:"method",key:"changeRemote",value:function(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_remote_access"})}},{kind:"method",key:"enableGatePariringByPin",value:function(){this.hass.callService("ais_cloud","enable_gate_pairing_by_pin")}},{kind:"method",key:"firstUpdated",value:function(){this._generateQR()}},{kind:"method",key:"render",value:function(){return this.remoteDomain="https://"+this.hass.states["sensor.ais_secure_android_id_dom"].state+".paczka.pro",r.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div .isWide=${this.isWide}>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Zdalny dostęp</span>
            <span slot="introduction"
              >W tej sekcji możesz skonfigurować zdalny dostęp do bramki</span
            >
            <ha-card header="Szyfrowany tunel">
              <div id="ha-switch-id">
                <ha-switch
                  .checked=${"on"===this.hass.states["input_boolean.ais_remote_access"].state}
                  @change=${this.changeRemote}
                ></ha-switch>
              </div>
              <div class="card-content">
                Tunel zapewnia bezpieczne zdalne połączenie z Twoim urządzeniem
                kiedy jesteś z dala od domu. Twoja bramka dostępna
                ${"on"===this.hass.states["input_boolean.ais_remote_access"].state?r.dy` jest `:" będzie "}
                z Internetu pod adresem
                <a href=${this.remoteDomain} target="_blank"
                  >${this.remoteDomain}</a
                >.
                <div
                  class="center-container border"
                  style="height: 320px; text-align: center;"
                >
                  <div id="qr" style="text-align: center; margin-top: 10px;">
                    ${this._qrCode?this._qrCode:r.dy`
                          <mwc-button @click=${this._generateQR}
                            >Pokaż kod QR
                          </mwc-button>
                        `}
                  </div>
                  Zeskanuj kod QR za pomocą aplikacji na telefonie.
                </div>
              </div>
              <div class="card-content" style="text-align:center;">
                <svg style="width:48px;height:48px" viewBox="0 0 24 24">
                  <path
                    fill="#929395"
                    d="M1,11H6L3.5,8.5L4.92,7.08L9.84,12L4.92,16.92L3.5,15.5L6,13H1V11M8,0H16L16.83,5H17A2,2 0 0,1 19,7V17C19,18.11 18.1,19 17,19H16.83L16,24H8L7.17,19H7C6.46,19 6,18.79 5.62,18.44L7.06,17H17V7H7.06L5.62,5.56C6,5.21 6.46,5 7,5H7.17L8,0Z"
                  />
                </svg>
                <br />
                ${"active"===this.hass.states["timer.ais_dom_pin_join"].state?r.dy`PIN aktywny przez dwie munuty: <br />
                      <span class="pin"
                        >${this.hass.states["sensor.gate_pairing_pin"].state}</span
                      ><br /> `:r.dy`<br />
                      <mwc-button @click=${this.enableGatePariringByPin}
                        >Generuj kod PIN</mwc-button
                      >`}
              </div>
              <div class="card-actions">
                <a
                  href="https://www.ai-speaker.com/docs/ais_bramka_remote_www_index"
                  target="_blank"
                >
                  <mwc-button>Dowiedz się jak to działa</mwc-button>
                </a>
              </div>
            </ha-card>

            <ais-webhooks .hass=${this.hass}></ais-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[r.iv`
        .content {
          padding-bottom: 32px;
        }
        a {
          color: var(--primary-color);
        }
        span.pin {
          color: var(--primary-color);
          font-size: 2em;
        }
        .border {
          margin-bottom: 12px;
          border-bottom: 2px solid rgba(0, 0, 0, 0.11);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-card > div#ha-switch-id {
          margin: -4px 0;
          position: absolute;
          right: 8px;
          top: 32px;
        }
        .card-actions a {
          text-decoration: none;
        }
      `]}}]}}),r.oi)},31203:(e,t,i)=>{"use strict";i.r(t);var r=i(15652),n=i(91168),o=i(83599),a=i(53658),s=(i(91476),i(75502));function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function y(e,t,i){return(y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(d)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,r.Mo)("hui-timer-entity-row")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_timeRemaining",value:void 0},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"setConfig",value:function(e){if(!e)throw new Error("Invalid configuration");this._config=e}},{kind:"method",key:"disconnectedCallback",value:function(){y(b(i.prototype),"disconnectedCallback",this).call(this),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){if(y(b(i.prototype),"connectedCallback",this).call(this),this._config&&this._config.entity){const e=this.hass.states[this._config.entity];e&&this._startInterval(e)}}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return r.dy``;const e=this.hass.states[this._config.entity];return e?r.dy`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        <div class="text-content">${this._computeDisplay(e)}</div>
      </hui-generic-entity-row>
    `:r.dy`
        <hui-warning>
          ${(0,s.i)(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"method",key:"shouldUpdate",value:function(e){return!!e.has("_timeRemaining")||(0,a.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(y(b(i.prototype),"updated",this).call(this,e),e.has("hass")){const t=this.hass.states[this._config.entity],i=e.get("hass");(i?i.states[this._config.entity]:void 0)!==t?this._startInterval(t):t||this._clearInterval()}}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(e){this._clearInterval(),this._calculateRemaining(e),"active"===e.state&&(this._interval=window.setInterval((()=>this._calculateRemaining(e)),1e3))}},{kind:"method",key:"_calculateRemaining",value:function(e){this._timeRemaining=(0,o.m)(e)}},{kind:"method",key:"_computeDisplay",value:function(e){if(!e)return null;if("idle"===e.state||0===this._timeRemaining)return this.hass.localize(`state.timer.${e.state}`)||e.state;let t=(0,n.Z)(this._timeRemaining||0);return"paused"===e.state&&(t+=` (${this.hass.localize("state.timer.paused")})`),t}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.659370c99885e6de8bee.js.map