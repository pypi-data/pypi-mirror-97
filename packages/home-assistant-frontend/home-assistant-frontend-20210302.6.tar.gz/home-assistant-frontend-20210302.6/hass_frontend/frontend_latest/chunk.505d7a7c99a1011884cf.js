/*! For license information please see chunk.505d7a7c99a1011884cf.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8849,3098,1139],{18601:(e,t,n)=>{"use strict";n.d(t,{qN:()=>o.q,Wg:()=>r});var o=n(78220);class r extends o.H{createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(e){this.formElement&&this.formElement.setAttribute("aria-label",e)}firstUpdated(){super.firstUpdated(),this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}},14114:(e,t,n)=>{"use strict";n.d(t,{P:()=>o});const o=e=>(t,n)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,n)=>t.constructor._observers.set(n,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const n=this.constructor._observers.get(t);void 0!==n&&n.call(this,this[t],e)}))}}t.constructor._observers.set(n,e)}},43453:(e,t,n)=>{"use strict";n.d(t,{Y:()=>a});n(43437);var o=/\.splices$/,r=/\.length$/,i=/\.?#?([0-9]+)$/;const a={properties:{data:{type:Object,notify:!0,value:function(){return this.zeroValue}},sequentialTransactions:{type:Boolean,value:!1},log:{type:Boolean,value:!1}},observers:["__dataChanged(data.*)"],created:function(){this.__initialized=!1,this.__syncingToMemory=!1,this.__initializingStoredValue=null,this.__transactionQueueAdvances=Promise.resolve()},ready:function(){this._initializeStoredValue()},get isNew(){return!0},get transactionsComplete(){return this.__transactionQueueAdvances},get zeroValue(){},saveValue:function(e){return Promise.resolve()},reset:function(){},destroy:function(){return this.data=this.zeroValue,this.saveValue()},initializeStoredValue:function(){return this.isNew?Promise.resolve():this._getStoredValue("data").then(function(e){if(this._log("Got stored value!",e,this.data),null==e)return this._setStoredValue("data",this.data||this.zeroValue);this.syncToMemory((function(){this.set("data",e)}))}.bind(this))},getStoredValue:function(e){return Promise.resolve()},setStoredValue:function(e,t){return Promise.resolve(t)},memoryPathToStoragePath:function(e){return e},storagePathToMemoryPath:function(e){return e},syncToMemory:function(e){this.__syncingToMemory||(this._group("Sync to memory."),this.__syncingToMemory=!0,e.call(this),this.__syncingToMemory=!1,this._groupEnd("Sync to memory."))},valueIsEmpty:function(e){return Array.isArray(e)?0===e.length:Object.prototype.isPrototypeOf(e)?0===Object.keys(e).length:null==e},_getStoredValue:function(e){return this.getStoredValue(this.memoryPathToStoragePath(e))},_setStoredValue:function(e,t){return this.setStoredValue(this.memoryPathToStoragePath(e),t)},_enqueueTransaction:function(e){if(this.sequentialTransactions)e=e.bind(this);else{var t=e.call(this);e=function(){return t}}return this.__transactionQueueAdvances=this.__transactionQueueAdvances.then(e).catch(function(e){this._error("Error performing queued transaction.",e)}.bind(this))},_log:function(...e){this.log&&console.log.apply(console,e)},_error:function(...e){this.log&&console.error.apply(console,e)},_group:function(...e){this.log&&console.group.apply(console,e)},_groupEnd:function(...e){this.log&&console.groupEnd.apply(console,e)},_initializeStoredValue:function(){if(!this.__initializingStoredValue){this._group("Initializing stored value.");var e=this.__initializingStoredValue=this.initializeStoredValue().then(function(){this.__initialized=!0,this.__initializingStoredValue=null,this._groupEnd("Initializing stored value.")}.bind(this)).catch(function(e){this.__initializingStoredValue=null,this._groupEnd("Initializing stored value.")}.bind(this));return this._enqueueTransaction((function(){return e}))}},__dataChanged:function(e){if(!this.isNew&&!this.__syncingToMemory&&this.__initialized&&!this.__pathCanBeIgnored(e.path)){var t=this.__normalizeMemoryPath(e.path),n=e.value,o=n&&n.indexSplices;this._enqueueTransaction((function(){return this._log("Setting",t+":",o||n),o&&this.__pathIsSplices(t)&&(t=this.__parentPath(t),n=this.get(t)),this._setStoredValue(t,n)}))}},__normalizeMemoryPath:function(e){for(var t=e.split("."),n=[],o=[],r=[],i=0;i<t.length;++i)o.push(t[i]),/^#/.test(t[i])?r.push(this.get(n).indexOf(this.get(o))):r.push(t[i]),n.push(t[i]);return r.join(".")},__parentPath:function(e){var t=e.split(".");return t.slice(0,t.length-1).join(".")},__pathCanBeIgnored:function(e){return r.test(e)&&Array.isArray(this.get(this.__parentPath(e)))},__pathIsSplices:function(e){return o.test(e)&&Array.isArray(this.get(this.__parentPath(e)))},__pathRefersToArray:function(e){return(o.test(e)||r.test(e))&&Array.isArray(this.get(this.__parentPath(e)))},__pathTailToIndex:function(e){var t=e.split(".").pop();return window.parseInt(t.replace(i,"$1"),10)}}},8878:(e,t,n)=>{"use strict";n(43437),n(8621),n(63207),n(30879),n(78814),n(60748),n(57548),n(73962);var o=n(51644),r=n(26110),i=n(21006),a=n(98235),s=n(9672),l=n(87156),c=n(81668),p=n(50856);(0,s.k)({_template:p.d`
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
`,is:"paper-dropdown-menu",behaviors:[o.P,r.a,i.V,a.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,l.vz)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},25782:(e,t,n)=>{"use strict";n(43437),n(65660),n(70019),n(97968);var o=n(9672),r=n(50856),i=n(33760);(0,o.k)({_template:r.d`
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
`,is:"paper-icon-item",behaviors:[i.U]})},33760:(e,t,n)=>{"use strict";n.d(t,{U:()=>i});n(43437);var o=n(51644),r=n(26110);const i=[o.P,r.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(e,t,n)=>{"use strict";n(43437),n(65660),n(70019);var o=n(9672),r=n(50856);(0,o.k)({_template:r.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(e,t,n)=>{"use strict";n(65660),n(70019);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(o.content)},53973:(e,t,n)=>{"use strict";n(43437),n(65660),n(97968);var o=n(9672),r=n(50856),i=n(33760);(0,o.k)({_template:r.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[i.U]})},51095:(e,t,n)=>{"use strict";n(43437);var o=n(78161),r=n(9672),i=n(50856);(0,r.k)({_template:i.d`
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
`,is:"paper-listbox",behaviors:[o.i],hostAttributes:{role:"listbox"}})},4268:(e,t,n)=>{"use strict";function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function a(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},i=Object.keys(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}function*s(e,t){!0===e||(!1===e?yield t.fail():yield*e)}function l(e){const{done:t,value:n}=e.next();return t?void 0:n}n.d(t,{DD:()=>p,Yj:()=>f,IX:()=>m,hu:()=>u,O7:()=>b,D8:()=>v,kE:()=>g,i0:()=>_,Rx:()=>O,Ry:()=>S,jt:()=>k,Z_:()=>x,n_:()=>j,dt:()=>P,G0:()=>A});class c{constructor(e){const{type:t,schema:n,coercer:o=(e=>e),validator:r=(()=>[]),refiner:i=(()=>[])}=e;this.type=t,this.schema=n,this.coercer=o,this.validator=r,this.refiner=i}}class p extends TypeError{constructor(e,t){const{path:n,value:o,type:r,branch:i}=e,s=a(e,["path","value","type","branch"]);let l;super(`Expected a value of type \`${r}\`${n.length?` for \`${n.join(".")}\``:""} but received \`${JSON.stringify(o)}\`.`),this.value=o,Object.assign(this,s),this.type=r,this.path=n,this.branch=i,this.failures=function(){return l||(l=[e,...t]),l},this.stack=(new Error).stack,this.__proto__=p.prototype}}function u(e,t){const n=h(e,t);if(n[0])throw n[0]}function d(e,t){const n=t.coercer(e);return u(n,t),n}function h(e,t,n=!1){n&&(e=t.coercer(e));const o=y(e,t),r=l(o);if(r){return[new p(r,o),void 0]}return[void 0,e]}function*y(e,t,n=[],o=[]){const{type:r}=t,a={value:e,type:r,branch:o,path:n,fail:(t={})=>i({value:e,type:r,path:n,branch:[...o,e]},t),check:(e,t,r,i)=>y(e,t,void 0!==r?[...n,i]:n,void 0!==r?[...o,r]:o)},c=s(t.validator(e,a),a),p=l(c);p?(yield p,yield*c):yield*s(t.refiner(e,a),a)}function f(){return j("any",(()=>!0))}function m(e){return new c({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map((t=>d(t,e))):t,*validator(t,n){if(Array.isArray(t)){if(e)for(const[o,r]of t.entries())yield*n.check(r,e,t,o)}else yield n.fail()}})}function b(){return j("boolean",(e=>"boolean"==typeof e))}function v(e){return j("Dynamic<...>",((t,n)=>n.check(t,e(t,n))))}function g(e){return j(`Enum<${e.map(E)}>`,(t=>e.includes(t)))}function _(e){return j(`Literal<${E(e)}>`,(t=>t===e))}function w(){return j("never",(()=>!1))}function O(){return j("number",(e=>"number"==typeof e&&!isNaN(e)))}function S(e){const t=e?Object.keys(e):[],n=w();return new c({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?z(e):e=>e,*validator(o,r){if("object"==typeof o&&null!=o){if(e){const i=new Set(Object.keys(o));for(const n of t){i.delete(n);const t=e[n],a=o[n];yield*r.check(a,t,o,n)}for(const e of i){const t=o[e];yield*r.check(t,n,o,e)}}}else yield r.fail()}})}function k(e){return new c({type:`${e.type}?`,schema:e.schema,validator:(t,n)=>void 0===t||n.check(t,e)})}function x(){return j("string",(e=>"string"==typeof e))}function j(e,t){return new c({type:e,validator:t,schema:null})}function P(e){const t=Object.keys(e);return j(`Type<{${t.join(",")}}>`,(function*(n,o){if("object"==typeof n&&null!=n)for(const r of t){const t=e[r],i=n[r];yield*o.check(i,t,n,r)}else yield o.fail()}))}function A(e){return j(`${e.map((e=>e.type)).join(" | ")}`,(function*(t,n){for(const o of e){const[...e]=n.check(t,o);if(0===e.length)return}yield n.fail()}))}function E(e){return"string"==typeof e?`"${e.replace(/"/g,'"')}"`:`${e}`}function z(e){const t=Object.keys(e);return n=>{if("object"!=typeof n||null==n)return n;const o={},r=new Set(Object.keys(n));for(const i of t){r.delete(i);const t=e[i],a=n[i];o[i]=d(a,t)}for(const e of r)o[e]=n[e];return o}}}}]);
//# sourceMappingURL=chunk.505d7a7c99a1011884cf.js.map