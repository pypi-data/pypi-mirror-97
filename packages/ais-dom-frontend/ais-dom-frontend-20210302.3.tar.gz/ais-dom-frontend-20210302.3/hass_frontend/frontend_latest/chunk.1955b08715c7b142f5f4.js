(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6440],{1265:(t,a,o)=>{"use strict";o.d(a,{Z:()=>e});const e=(0,o(76389).o)((t=>class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},56440:(t,a,o)=>{"use strict";o.r(a);o(53268),o(12730);var e=o(50856),r=o(28426),s=(o(60010),o(38353),o(63081),o(1265));class n extends((0,s.Z)(r.H3)){static get template(){return e.d`
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
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
        .buttons {
          position: relative;
          width: 200px;
          height: 200px;
        }

        .button {
          position: absolute;
          width: 50px;
          height: 50px;
        }

        .arrow {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .arrow-up {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-bottom: 16px solid black;
        }

        .arrow-right {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-left: 16px solid black;
        }

        .arrow-left {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-right: 16px solid black;
        }

        .arrow-down {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-top: 16px solid black;
        }

        .down {
          bottom: 0;
          left: 75px;
        }

        .left {
          top: 75px;
          left: 0;
        }

        .right {
          top: 75px;
          right: 0;
        }

        .up {
          top: 0;
          left: 75px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia ekranu</span>
            <span slot="introduction"
              >Jeżeli obraz na monitorze lub telewizorze podłączonym do bramki
              za pomocą złącza HDMI jest ucięty lub przesunięty, to w tym
              miejscu możesz dostosować obraz do rozmiaru ekranu.</span
            >
            <ha-card header="Dostosuj obraz do rozmiaru ekranu">
              <div class="card-content">
                <div class="card-content" style="text-align: center;">
                  <div style="display: inline-block;">
                    <p>Powiększanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table; border:solid 1px;"
                    >
                      <button
                        class="button up"
                        data-value="top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button down"
                        data-value="bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                    </div>
                  </div>
                  <div
                    style="text-align: center; display: inline-block; margin: 30px;"
                  >
                    <p>Zmniejszanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table;"
                    >
                      <button
                        class="button up"
                        data-value="-top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <div
                        style="margin: 0 auto; height: 98px; width:98px; margin-top: 50px; margin-left: 50px; display: flex; border:solid 1px;"
                      ></div>
                      <button
                        class="button down"
                        data-value="-bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="-right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="-left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="card-actions" style="margin-top: 30px;">
                  <div>
                    <ha-icon-button
                      class="user-button"
                      icon="mdi:restore"
                      on-click="wmRestoreSettings"
                    ></ha-icon-button
                    ><mwc-button on-click="wmOverscan" data-value="reset"
                      >Reset ekranu do ustawień domyślnych</mwc-button
                    >
                  </div>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean}}ready(){super.ready()}wmOverscan(t){this.hass.callService("ais_shell_command","change_wm_overscan",{value:t.currentTarget.getAttribute("data-value")})}}customElements.define("ha-config-ais-dom-config-display",n)}}]);
//# sourceMappingURL=chunk.1955b08715c7b142f5f4.js.map