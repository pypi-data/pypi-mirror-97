(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-233c8b9c"],{"13f9":function(e,t,n){"use strict";n.r(t);var i=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("v-text-field",{staticClass:"linkField pb-1",attrs:{value:e.value?e.value[e.titleField||"title"]:"",label:e.label,"append-icon":"mdi-chevron-up",clearable:"","hide-details":"",disabled:e.readOnly,flat:"",readonly:"",autofocus:e.autofocus},on:{keydown:[function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:(t.stopPropagation(),e.emitAction({name:"Update"}))},function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"escape",void 0,t.key,void 0)?null:(t.stopPropagation(),e.emitAction({name:"Cancel"}))},function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"up",38,t.key,["Up","ArrowUp"])?null:(t.stopPropagation(),e.beginSelect(t))}],click:e.viewItem,"click:append":e.beginSelect,"click:clear":e.clearItem}}),e.selectionFormVisible?n(e.formHandler,{tag:"component",attrs:{"form-uid":e.formUid,"form-data":e.formData},on:{action:function(t){return e.onAction(t,"selectForm")}}}):e._e()],1)},o=[],a=(n("d3b7"),n("dce2")),c={name:"FieldLink",components:{RightDrawerFormViewer3:function(){return Promise.all([n.e("chunk-766f9425"),n.e("chunk-41e18aac")]).then(n.bind(null,"ef03"))}},mixins:[a["a"]],props:{value:{type:Object,default:function(){return{}}},formHandler:{type:String,default:"RightDrawerFormViewer3"},label:{type:String,default:""},titleField:{type:String,default:"title"},fields:{type:Array,default:function(){return[]}},formUid:{type:String,default:""},formData:{type:Object,default:function(){return{}}},multiSelect:{type:Boolean,default:!1},readOnly:{type:Boolean,default:!1},autofocus:{type:Boolean,default:!1}},data:function(){return{selectionFormVisible:!1}},methods:{viewItem:function(){},beginSelect:function(){this.selectionFormVisible=!0},clearItem:function(){this.$emit("input",null)},actionRowActivate:function(e){this.actionCloseForm(),this.$emit("input",e),console.log("input link-field "+e.row.title)},actionSelectItems:function(e){var t=null;e.length&&(t=this.multiSelect?e:e[0]),this.$emit("input",t),this.actionCloseForm()},actionCloseForm:function(e,t){this.selectionFormVisible=!1}}},r=c,l=n("2877"),u=n("6544"),s=n.n(u),d=n("8654"),m=Object(l["a"])(r,i,o,!1,null,null,null);t["default"]=m.exports;s()(m,{VTextField:d["a"]})},dce2:function(e,t,n){"use strict";n("99af"),n("b0c0"),n("96cf");var i=n("1da1");t["a"]={methods:{onAction:function(e,t){console.log("".concat(this.$options.name," on action ").concat(e.name));var n="action".concat(e.name);Object.prototype.hasOwnProperty.call(this,n)?this[n](e.data,t):this.emitAction(e.name,e.data)},emitAction:function(e,t){this.$emit("action",{name:e,data:t})},dispatchAction:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function n(){var i,o;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:return i=e.data||{},o=i.namespace||t.store.namespace,console.log("".concat(t.$options.name," dispatch action ").concat(o,"/").concat(e.name)),n.next=5,t.$store.dispatch("".concat(o,"/").concat(e.name),{store:t.store,params:t.params,data:e.data},{root:!0});case 5:case"end":return n.stop()}}),n)})))()}}}}}]);
//# sourceMappingURL=chunk-233c8b9c.2fa2a8cd.js.map