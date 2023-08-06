(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1666],{26765:(e,a,s)=>{"use strict";s.d(a,{Ys:()=>n,g7:()=>c,D9:()=>r});var t=s(47181);const o=()=>Promise.all([s.e(8200),s.e(879),s.e(2762),s.e(8345),s.e(6509),s.e(32)]).then(s.bind(s,1281)),i=(e,a,s)=>new Promise((i=>{const n=a.cancel,c=a.confirm;(0,t.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...a,...s,cancel:()=>{i(!!(null==s?void 0:s.prompt)&&null),n&&n()},confirm:e=>{i(!(null==s?void 0:s.prompt)||e),c&&c(e)}}})})),n=(e,a)=>i(e,a),c=(e,a)=>i(e,a,{confirmation:!0}),r=(e,a)=>i(e,a,{prompt:!0})},28490:(e,a,s)=>{"use strict";s.r(a);s(53268),s(12730);var t=s(50856),o=s(28426);s(60010),s(38353),s(63081),s(54909);class i extends o.H3{static get template(){return t.d`
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
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Wyłączenie bramki</span>
            <span slot="introduction"
              >W tej sekcji możesz zrestartować lub całkowicie wyłączyć bramkę
            </span>
            <ha-card header="Restart lub wyłączenie">
              <div class="card-content">
                W tej sekcji możesz zrestartować lub całkowicie wyłączyć bramkę
              </div>
              <div class="card-actions warning">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:refresh"
                  ></ha-icon-button>
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="script"
                    service="ais_restart_system"
                    >Uruchom ponownie
                  </ha-call-service-button>
                </div>
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:stop"
                  ></ha-icon-button>
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="script"
                    service="ais_stop_system"
                    >Wyłącz
                  </ha-call-service-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean}}computeClasses(e){return e?"content":"content narrow"}}customElements.define("ha-config-ais-dom-config-power",i)}}]);
//# sourceMappingURL=chunk.8366cf562078ab4361ca.js.map