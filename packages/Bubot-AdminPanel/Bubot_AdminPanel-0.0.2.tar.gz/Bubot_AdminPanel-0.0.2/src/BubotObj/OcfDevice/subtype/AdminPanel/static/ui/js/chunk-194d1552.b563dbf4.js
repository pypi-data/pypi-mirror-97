(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-194d1552"],{"0fd9":function(t,e,n){"use strict";n("99af"),n("4160"),n("caad"),n("13d5"),n("4ec9"),n("b64b"),n("d3b7"),n("ac1f"),n("2532"),n("3ca3"),n("5319"),n("159b"),n("ddb0");var a=n("ade3"),i=n("5530"),s=(n("4b85"),n("2b0e")),r=n("d9f7"),o=n("80d2"),l=["sm","md","lg","xl"],c=["start","end","center"];function u(t,e){return l.reduce((function(n,a){return n[t+Object(o["D"])(a)]=e(),n}),{})}var d=function(t){return[].concat(c,["baseline","stretch"]).includes(t)},h=u("align",(function(){return{type:String,default:null,validator:d}})),f=function(t){return[].concat(c,["space-between","space-around"]).includes(t)},v=u("justify",(function(){return{type:String,default:null,validator:f}})),b=function(t){return[].concat(c,["space-between","space-around","stretch"]).includes(t)},p=u("alignContent",(function(){return{type:String,default:null,validator:b}})),m={align:Object.keys(h),justify:Object.keys(v),alignContent:Object.keys(p)},g={align:"align",justify:"justify",alignContent:"align-content"};function y(t,e,n){var a=g[t];if(null!=n){if(e){var i=e.replace(t,"");a+="-".concat(i)}return a+="-".concat(n),a.toLowerCase()}}var O=new Map;e["a"]=s["a"].extend({name:"v-row",functional:!0,props:Object(i["a"])(Object(i["a"])(Object(i["a"])({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:d}},h),{},{justify:{type:String,default:null,validator:f}},v),{},{alignContent:{type:String,default:null,validator:b}},p),render:function(t,e){var n=e.props,i=e.data,s=e.children,o="";for(var l in n)o+=String(n[l]);var c=O.get(o);return c||function(){var t,e;for(e in c=[],m)m[e].forEach((function(t){var a=n[t],i=y(e,t,a);i&&c.push(i)}));c.push((t={"no-gutters":n.noGutters,"row--dense":n.dense},Object(a["a"])(t,"align-".concat(n.align),n.align),Object(a["a"])(t,"justify-".concat(n.justify),n.justify),Object(a["a"])(t,"align-content-".concat(n.alignContent),n.alignContent),t)),O.set(o,c)}(),t(n.tag,Object(r["a"])(i,{staticClass:"row",class:c}),s)}})},"16b7":function(t,e,n){"use strict";n("a9e3");var a=n("2b0e");e["a"]=a["a"].extend().extend({name:"delayable",props:{openDelay:{type:[Number,String],default:0},closeDelay:{type:[Number,String],default:0}},data:function(){return{openTimeout:void 0,closeTimeout:void 0}},methods:{clearDelay:function(){clearTimeout(this.openTimeout),clearTimeout(this.closeTimeout)},runDelay:function(t,e){var n=this;this.clearDelay();var a=parseInt(this["".concat(t,"Delay")],10);this["".concat(t,"Timeout")]=setTimeout(e||function(){n.isActive={open:!0,close:!1}[t]},a)}}})},"22da":function(t,e,n){"use strict";var a=n("490a");e["a"]=a["a"]},3978:function(t,e,n){"use strict";n.r(e);var a=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-card",{staticClass:"pa-0 ma-0",attrs:{flat:""}},[n("v-card-actions",{staticClass:"pa-0 pb-1"},[n("div",{staticClass:"pa-0 ma-0 pt-4"},[n("v-btn",{attrs:{icon:"",dense:""},on:{click:function(e){t.show=!t.show}}},[n("v-icon",[t._v(t._s(t.show?"mdi-minus-box-outline":"mdi-plus-box-outline"))])],1)],1),n("v-text-field",{attrs:{label:(t.schema.title||t.elemName)+" ["+t.elemValue.length+"]",placeholder:t.schema["description"],flat:"","hide-details":"",disabled:"",value:t.title}}),t.readOnly?t._e():n("div",{staticClass:"pa-0 ma-0 pt-4"},[t.show?n("v-btn",{attrs:{dense:"",icon:"",disabled:t.readOnly}},[n("v-icon",[t._v(t._s("mdi-plus-circle"))])],1):t._e()],1)],1),n("v-expand-transition",[n("v-card",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"ml-4 pb-1 pl-2",staticStyle:{"border-left":"1px solid var(--v-delimiter-base)"},attrs:{flat:"",tile:""}},t._l(t.elemValue,(function(e,a){return n("span",{key:""+t.path+t.delimiter+a},[n("v-hover",{scopedSlots:t._u([{key:"default",fn:function(i){var s=i.hover;return[n("v-row",{staticClass:"pl-2",staticStyle:{"flex-wrap":"nowrap"},attrs:{"no-gutters":""}},[n("JsonElem",{staticClass:"flex-grow-1 flex-shrink-0",staticStyle:{"min-width":"100px","max-width":"100%"},attrs:{"elem-value":e,"elem-name":"",schema:t.schema.items,path:(t.path?t.path+t.delimiter:"")+a,"input-listeners":t.inputListeners,"array-elem":!0,level:t.level+1,"read-only":t.readOnly?t.readOnly:t.schema.readOnly,"hide-read-only":t.hideReadOnly}}),t.readOnly?t._e():n("v-btn",{staticClass:"flex-grow-0 flex-shrink-1",attrs:{dense:"",icon:"",disabled:t.readOnly}},[s?n("v-icon",{on:{click:function(e){return t.deleteItem(a)}}},[t._v(" "+t._s("mdi-delete")+" ")]):t._e()],1)],1)]}}],null,!0)})],1)})),0)],1)],1)},i=[],s=(n("a9e3"),n("d3b7"),{components:{JsonElem:function(){return Promise.resolve().then(n.bind(null,"3c48"))}},props:{schema:Object,elemValue:Array,elemName:String,path:String,inputListeners:Object,arrayElem:Boolean,level:Number,readOnly:Boolean,hideReadOnly:Boolean},data:function(){return{show:!1,delimiter:"."}},computed:{arrayLen:function(){return this.elemValue.length},title:function(){var t="";if(!this.elemValue)return"";for(var e="",n=0;n<=Math.min(this.elemValue.length-1,1);n++){switch(this.schema.items.type){case"string":e=this.elemValue[n];break;case"object":e=this.elemValue[n][this.schema.items["titleField"]||"title"];break;default:return""}t&&(t+=", "),t+=e}return this.elemValue.length>2&&(t+=", ..."),t}},methods:{deleteItem:function(t){this.$emit("action",{name:"UpdateProp",data:{action:"delete",path:this.path,value:t}})}}}),r=s,o=(n("95ac"),n("2877")),l=n("6544"),c=n.n(l),u=n("8336"),d=n("b0af"),h=n("99d9"),f=n("0789"),v=n("ce87"),b=n("132d"),p=n("0fd9"),m=n("8654"),g=Object(o["a"])(r,a,i,!1,null,"357f6692",null);e["default"]=g.exports;c()(g,{VBtn:u["a"],VCard:d["a"],VCardActions:h["a"],VExpandTransition:f["a"],VHover:v["a"],VIcon:b["a"],VRow:p["a"],VTextField:m["a"]})},"490a":function(t,e,n){"use strict";n("99af"),n("a9e3"),n("8d4f");var a=n("a9ad"),i=n("80d2");e["a"]=a["a"].extend({name:"v-progress-circular",props:{button:Boolean,indeterminate:Boolean,rotate:{type:[Number,String],default:0},size:{type:[Number,String],default:32},width:{type:[Number,String],default:4},value:{type:[Number,String],default:0}},data:function(){return{radius:20}},computed:{calculatedSize:function(){return Number(this.size)+(this.button?8:0)},circumference:function(){return 2*Math.PI*this.radius},classes:function(){return{"v-progress-circular--indeterminate":this.indeterminate,"v-progress-circular--button":this.button}},normalizedValue:function(){return this.value<0?0:this.value>100?100:parseFloat(this.value)},strokeDashArray:function(){return Math.round(1e3*this.circumference)/1e3},strokeDashOffset:function(){return(100-this.normalizedValue)/100*this.circumference+"px"},strokeWidth:function(){return Number(this.width)/+this.size*this.viewBoxSize*2},styles:function(){return{height:Object(i["g"])(this.calculatedSize),width:Object(i["g"])(this.calculatedSize)}},svgStyles:function(){return{transform:"rotate(".concat(Number(this.rotate),"deg)")}},viewBoxSize:function(){return this.radius/(1-Number(this.width)/+this.size)}},methods:{genCircle:function(t,e){return this.$createElement("circle",{class:"v-progress-circular__".concat(t),attrs:{fill:"transparent",cx:2*this.viewBoxSize,cy:2*this.viewBoxSize,r:this.radius,"stroke-width":this.strokeWidth,"stroke-dasharray":this.strokeDashArray,"stroke-dashoffset":e}})},genSvg:function(){var t=[this.indeterminate||this.genCircle("underlay",0),this.genCircle("overlay",this.strokeDashOffset)];return this.$createElement("svg",{style:this.svgStyles,attrs:{xmlns:"http://www.w3.org/2000/svg",viewBox:"".concat(this.viewBoxSize," ").concat(this.viewBoxSize," ").concat(2*this.viewBoxSize," ").concat(2*this.viewBoxSize)}},t)},genInfo:function(){return this.$createElement("div",{staticClass:"v-progress-circular__info"},this.$slots.default)}},render:function(t){return t("div",this.setTextColor(this.color,{staticClass:"v-progress-circular",attrs:{role:"progressbar","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":this.indeterminate?void 0:this.normalizedValue},class:this.classes,style:this.styles,on:this.$listeners}),[this.genSvg(),this.genInfo()])}})},"4b85":function(t,e,n){},"4e82":function(t,e,n){"use strict";n.d(e,"a",(function(){return s}));var a=n("ade3"),i=n("3206");function s(t,e,n){var s=Object(i["a"])(t,e,n).extend({name:"groupable",props:{activeClass:{type:String,default:function(){if(this[t])return this[t].activeClass}},disabled:Boolean},data:function(){return{isActive:!1}},computed:{groupClasses:function(){return this.activeClass?Object(a["a"])({},this.activeClass,this.isActive):{}}},created:function(){this[t]&&this[t].register(this)},beforeDestroy:function(){this[t]&&this[t].unregister(this)},methods:{toggle:function(){this.$emit("change")}}});return s}s("itemGroup")},"615b":function(t,e,n){},8336:function(t,e,n){"use strict";n("4160"),n("caad"),n("c7cd");var a=n("53ca"),i=n("3835"),s=n("5530"),r=(n("86cc"),n("10d2")),o=n("22da"),l=n("4e82"),c=n("f2e7"),u=n("fe6c"),d=n("1c87"),h=n("af2b"),f=n("58df"),v=n("d9bd"),b=Object(f["a"])(r["a"],d["a"],u["a"],h["a"],Object(l["a"])("btnToggle"),Object(c["b"])("inputValue"));e["a"]=b.extend().extend({name:"v-btn",props:{activeClass:{type:String,default:function(){return this.btnToggle?this.btnToggle.activeClass:""}},block:Boolean,depressed:Boolean,fab:Boolean,icon:Boolean,loading:Boolean,outlined:Boolean,retainFocusOnClick:Boolean,rounded:Boolean,tag:{type:String,default:"button"},text:Boolean,tile:Boolean,type:{type:String,default:"button"},value:null},data:function(){return{proxyClass:"v-btn--active"}},computed:{classes:function(){return Object(s["a"])(Object(s["a"])(Object(s["a"])(Object(s["a"])(Object(s["a"])({"v-btn":!0},d["a"].options.computed.classes.call(this)),{},{"v-btn--absolute":this.absolute,"v-btn--block":this.block,"v-btn--bottom":this.bottom,"v-btn--contained":this.contained,"v-btn--depressed":this.depressed||this.outlined,"v-btn--disabled":this.disabled,"v-btn--fab":this.fab,"v-btn--fixed":this.fixed,"v-btn--flat":this.isFlat,"v-btn--icon":this.icon,"v-btn--left":this.left,"v-btn--loading":this.loading,"v-btn--outlined":this.outlined,"v-btn--right":this.right,"v-btn--round":this.isRound,"v-btn--rounded":this.rounded,"v-btn--router":this.to,"v-btn--text":this.text,"v-btn--tile":this.tile,"v-btn--top":this.top},this.themeClasses),this.groupClasses),this.elevationClasses),this.sizeableClasses)},contained:function(){return Boolean(!this.isFlat&&!this.depressed&&!this.elevation)},computedRipple:function(){var t=!this.icon&&!this.fab||{circle:!0};return!this.disabled&&(null!=this.ripple?this.ripple:t)},isFlat:function(){return Boolean(this.icon||this.text||this.outlined)},isRound:function(){return Boolean(this.icon||this.fab)},styles:function(){return Object(s["a"])({},this.measurableStyles)}},created:function(){var t=this,e=[["flat","text"],["outline","outlined"],["round","rounded"]];e.forEach((function(e){var n=Object(i["a"])(e,2),a=n[0],s=n[1];t.$attrs.hasOwnProperty(a)&&Object(v["a"])(a,s,t)}))},methods:{click:function(t){!this.retainFocusOnClick&&!this.fab&&t.detail&&this.$el.blur(),this.$emit("click",t),this.btnToggle&&this.toggle()},genContent:function(){return this.$createElement("span",{staticClass:"v-btn__content"},this.$slots.default)},genLoader:function(){return this.$createElement("span",{class:"v-btn__loader"},this.$slots.loader||[this.$createElement(o["a"],{props:{indeterminate:!0,size:23,width:2}})])}},render:function(t){var e=[this.genContent(),this.loading&&this.genLoader()],n=this.isFlat?this.setTextColor:this.setBackgroundColor,i=this.generateRouteLink(),s=i.tag,r=i.data;return"button"===s&&(r.attrs.type=this.type,r.attrs.disabled=this.disabled),r.attrs.value=["string","number"].includes(Object(a["a"])(this.value))?this.value:JSON.stringify(this.value),t(s,this.disabled?r:n(this.color,r),e)}})},"86cc":function(t,e,n){},"8d4f":function(t,e,n){},"8e1b":function(t,e,n){},"95ac":function(t,e,n){"use strict";var a=n("8e1b"),i=n.n(a);i.a},"99d9":function(t,e,n){"use strict";n.d(e,"a",(function(){return s}));var a=n("b0af"),i=n("80d2"),s=Object(i["h"])("v-card__actions"),r=Object(i["h"])("v-card__subtitle"),o=Object(i["h"])("v-card__text"),l=Object(i["h"])("v-card__title");a["a"]},b0af:function(t,e,n){"use strict";n("0481"),n("4069"),n("a9e3");var a=n("5530"),i=(n("615b"),n("10d2")),s=n("297c"),r=n("1c87"),o=n("58df");e["a"]=Object(o["a"])(s["a"],r["a"],i["a"]).extend({name:"v-card",props:{flat:Boolean,hover:Boolean,img:String,link:Boolean,loaderHeight:{type:[Number,String],default:4},raised:Boolean},computed:{classes:function(){return Object(a["a"])(Object(a["a"])({"v-card":!0},r["a"].options.computed.classes.call(this)),{},{"v-card--flat":this.flat,"v-card--hover":this.hover,"v-card--link":this.isClickable,"v-card--loading":this.loading,"v-card--disabled":this.disabled,"v-card--raised":this.raised},i["a"].options.computed.classes.call(this))},styles:function(){var t=Object(a["a"])({},i["a"].options.computed.styles.call(this));return this.img&&(t.background='url("'.concat(this.img,'") center center / cover no-repeat')),t}},methods:{genProgress:function(){var t=s["a"].options.methods.genProgress.call(this);return t?this.$createElement("div",{staticClass:"v-card__progress",key:"progress"},[t]):null}},render:function(t){var e=this.generateRouteLink(),n=e.tag,a=e.data;return a.style=this.styles,this.isClickable&&(a.attrs=a.attrs||{},a.attrs.tabindex=0),t(n,this.setBackgroundColor(this.color,a),[this.genProgress(),this.$slots.default])}})},ce87:function(t,e,n){"use strict";var a=n("16b7"),i=n("f2e7"),s=n("58df"),r=n("d9bd");e["a"]=Object(s["a"])(a["a"],i["a"]).extend({name:"v-hover",props:{disabled:{type:Boolean,default:!1},value:{type:Boolean,default:void 0}},methods:{onMouseEnter:function(){this.runDelay("open")},onMouseLeave:function(){this.runDelay("close")}},render:function(){return this.$scopedSlots.default||void 0!==this.value?(this.$scopedSlots.default&&(t=this.$scopedSlots.default({hover:this.isActive})),Array.isArray(t)&&1===t.length&&(t=t[0]),t&&!Array.isArray(t)&&t.tag?(this.disabled||(t.data=t.data||{},this._g(t.data,{mouseenter:this.onMouseEnter,mouseleave:this.onMouseLeave})),t):(Object(r["c"])("v-hover should only contain a single element",this),t)):(Object(r["c"])("v-hover is missing a default scopedSlot or bound value",this),null);var t}})},f2e7:function(t,e,n){"use strict";n.d(e,"b",(function(){return s}));var a=n("ade3"),i=n("2b0e");function s(){var t,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"value",n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"input";return i["a"].extend({name:"toggleable",model:{prop:e,event:n},props:Object(a["a"])({},e,{required:!1}),data:function(){return{isActive:!!this[e]}},watch:(t={},Object(a["a"])(t,e,(function(t){this.isActive=!!t})),Object(a["a"])(t,"isActive",(function(t){!!t!==this[e]&&this.$emit(n,t)})),t)})}var r=s();e["a"]=r}}]);
//# sourceMappingURL=chunk-194d1552.b563dbf4.js.map