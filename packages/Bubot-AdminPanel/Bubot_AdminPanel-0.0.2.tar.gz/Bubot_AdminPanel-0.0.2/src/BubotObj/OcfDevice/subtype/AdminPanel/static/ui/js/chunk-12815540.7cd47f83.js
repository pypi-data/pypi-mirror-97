(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-12815540"],{2275:function(e,t,r){"use strict";r("96cf");var n=r("1da1"),a=r("e8ba"),i=r("bd10"),c=r("8bb9"),o=r("4198");t["a"]={namespaced:!0,state:{},getters:{mode:o["b"],getProps:o["a"]},mutations:{initStoreKey:c["a"],updateItemProps:c["b"],loading:function(e,t){var r=t.uid,n=t.loading,a=t.item;e[r]={loading:n,item:a}}},actions:{initForm:i["b"],error:i["a"],read:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r){var n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t.commit("loading",{uid:r.store.uid,item:{},loading:!0}),e.next=3,Object(a["a"])("read",t,r);case 3:n=e.sent,t.commit("loading",{uid:r.store.uid,item:n,loading:!1});case 5:case"end":return e.stop()}}),e)})));function t(t,r){return e.apply(this,arguments)}return t}(),update:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r.data=t.state[r.store.uid].item,e.next=3,Object(a["a"])("update",t,r);case 3:case"end":return e.stop()}}),e)})));function t(t,r){return e.apply(this,arguments)}return t}()}}},"5d41":function(e,t,r){var n=r("23e7"),a=r("861d"),i=r("825a"),c=r("5135"),o=r("06cf"),s=r("e163");function u(e,t){var r,n,l=arguments.length<3?e:arguments[2];return i(e)===l?e[t]:(r=o.f(e,t))?c(r,"value")?r.value:void 0===r.get?void 0:r.get.call(l):a(n=s(e))?u(n,t,l):void 0}n({target:"Reflect",stat:!0},{get:u})},7577:function(e,t,r){},"97f7":function(e,t,r){"use strict";r("96cf");var n=r("1da1"),a=r("bc3a"),i=r.n(a),c=r("2b0e");t["a"]={namespaced:!0,state:{},mutations:{schema:function(e,t){var r=t.uid,n=t.schema;c["a"].set(e,r,n)}},actions:{read:function(e,t){return Object(n["a"])(regeneratorRuntime.mark((function r(){var n,a;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(t){r.next=2;break}return r.abrupt("return",{});case 2:if(!Object.prototype.hasOwnProperty.call(e.state,t)){r.next=8;break}return r.next=5,e.state[t];case 5:return r.abrupt("return",r.sent);case 8:return console.log("load scheme "+t),n={},r.prev=10,r.next=13,i.a.get("/api/".concat(e.rootState.app,"/OcfSchema/read"),{params:{id:t}});case 13:a=r.sent,n=a.data,r.next=20;break;case 17:r.prev=17,r.t0=r["catch"](10),n={};case 20:return e.commit("schema",{uid:t,schema:n}),r.abrupt("return",n);case 22:case"end":return r.stop()}}),r,null,[[10,17]])})))()}}}},a729:function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",{staticClass:"pa-0 ma-0"},[r("v-progress-linear",{attrs:{indeterminate:e.loading,height:"2","background-color":"header1_bg"}}),r("PanelToolBar",{attrs:{"tool-bar":e.toolBar,"header-value":e.title,"edit-header":!0,loading:e.loading},on:{action:e.onAction}}),e.loading?e._e():r("v-container",{staticClass:"pa-4 ma-0"},[e.mainRes.length?r("v-container",{staticClass:"pa-0 ma-0"},e._l(e.mainRes,(function(t,n){return r("OcfResourceTmpl",{key:n,attrs:{res:e.itemFull.links[t],href:t},on:{action:e.onAction}})})),1):e._e(),e.serviceRes.length?r("div",{staticClass:"text-h6 py-2"},[e._v(" "+e._s(e.$t("ocfServiceResTitle"))+" ")]):e._e(),e.serviceRes.length?r("v-container",{staticClass:"pa-0 ma-0"},e._l(e.serviceRes,(function(t,n){return r("OcfResourceTmpl",{key:n,attrs:{res:e.itemFull.links[t],href:t},on:{action:e.onAction}})})),1):e._e()],1),e.actionForm&&e.actionForm.visible?r(e.actionForm.handler||"RightDrawerFormViewer2",{tag:"component",attrs:{"form-uid":e.actionForm.formUid,visible:e.actionForm.visible},on:{action:function(t){return e.onAction(t,"actionForm")}}}):e._e()],1)},a=[],i=(r("4de4"),r("7db0"),r("b0c0"),r("d3b7"),r("ddb0"),r("96cf"),r("1da1")),c=r("bf28"),o=r("dce2"),s=r("8f74"),u=r("b39e"),l=r("2275"),p=r("97f7"),h={name:"OcfDriver",components:{OcfResourceTmpl:function(){return Promise.all([r.e("chunk-75f0404a"),r.e("chunk-f984ecc2"),r.e("chunk-2c33c399"),r.e("chunk-2d0b6eb6")]).then(r.bind(null,"1ee1"))},PanelToolBar:function(){return Promise.all([r.e("chunk-75f0404a"),r.e("chunk-f984ecc2"),r.e("chunk-5bb29098"),r.e("chunk-52fcaa94"),r.e("chunk-03738786")]).then(r.bind(null,"7d5d"))}},mixins:[c["a"],o["a"]],props:{toolBar:{type:Object,default:function(){return{items:[]}}},defaultAction:{type:Object,default:function(){return{}}},dataSource:{type:Object,default:function(){return{}}},item:{type:Object,default:function(){return{}}}},data:function(){return{visible:!1,loading:!1,active:[],avatar:null,open:[],props_schema:null,props_data:null,source:null,itemFull:{},resIndex:{},mainRes:[],serviceRes:[],actionForm:{}}},computed:{title:function(){return this.itemFull&&this.itemFull.links?this.itemFull.links["/oic/d"]["n"]:this.item["n"]},items:function(){return this.props},resources:function(){try{return this.item.links}catch(e){return[]}},selected:function(){if(this.active.length){var e=this.active[0];return this.users.find((function(t){return t.id===e}))}},uid:function(){if(this.item&&this.source&&this.source.keyProperty)return this.item[this.source.keyProperty]}},watch:{uid:function(e){e&&this.init()},dataSource:function(){this.source=Object(u["a"])(this.dataSource,this.$store)}},beforeMount:function(){var e=this;return Object(i["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.source=Object(u["a"])(e.dataSource,e.$store);case 1:case"end":return t.stop()}}),t)})))()},beforeCreate:function(){Object(s["c"])(this.$store.state,this.$options.name)||this.$store.registerModule(this.$options.name,l["a"]),Object(s["c"])(this.$store.state,"OcfSchema")||this.$store.registerModule("OcfSchema",p["a"])},methods:{init:function(){var e=this;return Object(i["a"])(regeneratorRuntime.mark((function t(){var r,n,a,i;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(e.itemFull=Object(s["e"])({},e.item),e.resIndex={},e.mainRes=[],e.serviceRes=[],r=e.itemFull["links"],!r){t.next=25;break}t.t0=regeneratorRuntime.keys(r);case 7:if((t.t1=t.t0()).done){t.next=23;break}if(n=t.t1.value,!Object.prototype.hasOwnProperty.call(r,n)){t.next=21;break}if(a="ocfServiceRes.".concat(n),t.prev=11,0!==r[n]["p"]["bm"]){t.next=14;break}return t.abrupt("continue",7);case 14:t.next=18;break;case 16:t.prev=16,t.t2=t["catch"](11);case 18:i=e.mainRes,i=e.$t(a)===a?e.mainRes:e.serviceRes,i.push(n);case 21:t.next=7;break;case 23:e.mainRes=e.mainRes.sort(),e.serviceRes=e.serviceRes.sort();case 25:case"end":return t.stop()}}),t,null,[[11,16]])})))()},actionUpdateHeader:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:"change"===e.data.action&&(t.itemFull.links["/oic/d"]["n"]=e.data.value);case 1:case"end":return r.stop()}}),r)})))()},actionSelectItem:function(e,t){console.log},actionCallDataSourceForSelectedItems:function(e){var t,r=Object(s["e"])({data:{}},e);t=Object(s["c"])(e,"dataSource")?Object(u["a"])(e.dataSource,this.$store):this.source,r.data.items=[this.itemFull],r.data.filter=null,t.call(r)},actionUpdateRes:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:t.itemFull.links[e["href"]]=e["res"];case 1:case"end":return r.stop()}}),r)})))()},actionShowSelectForm:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:t.actionForm=e;case 1:case"end":return r.stop()}}),r)})))()},actionCloseForm:function(e,t){"actionForm"===t?this.actionForm.visible=!1:this.emitAction("CloseForm",e)}}},f=h,d=(r("b477"),r("2877")),m=r("6544"),b=r.n(m),v=r("a523"),g=r("8e36"),w=Object(d["a"])(f,n,a,!1,null,null,null);t["default"]=w.exports;b()(w,{VContainer:v["a"],VProgressLinear:g["a"]})},b39e:function(e,t,r){"use strict";r.d(t,"a",(function(){return O}));var n=r("8f74"),a=(r("99af"),r("4de4"),r("c975"),r("fb6a"),r("b0c0"),r("96cf"),r("1da1")),i=r("d4ec"),c=r("bee2"),o=r("257e"),s=r("262e"),u=r("2caf"),l=r("ade3"),p=function(){function e(t,r){Object(i["a"])(this,e),Object(l["a"])(this,"rawData",[]),Object(l["a"])(this,"filteredRawData",[]),Object(l["a"])(this,"total",0),Object(l["a"])(this,"rows",[]),Object(l["a"])(this,"props",{rows:[],page:1,filter:{},itemsPerPage:25,appName:"",objName:"",dataTableOptions:{},filterFields:[],keyProperty:"id"}),Object(l["a"])(this,"store",void 0),Object(l["a"])(this,"keyProperty",void 0),Object(l["a"])(this,"loading",!1),Object(l["a"])(this,"filterFields",[]),this.props.appName=r.state.app,this.store=r,this.changeProps(t),this.rawData=this.props.rows||[],this.keyProperty=this.props.keyProperty||"id"}return Object(c["a"])(e,[{key:"changeProps",value:function(e){this.props=Object(n["e"])(this.props,e)}},{key:"changeFilter",value:function(e){this.props.filter=Object(n["e"])(this.props.filter,e),this.props.dataTableOptions.page=1,this.query()}},{key:"query",value:function(){throw new Error("method query not implemented in source class")}},{key:"call",value:function(){throw new Error("method call not implemented in source class")}},{key:"read",value:function(){throw new Error("method read not implemented in source class")}}]),e}(),h={equals:function(e,t,r){return r[e["name"]]===t},in:function(e,t,r){return!(t[0]&&r[e["name"]]<t[0])&&!(t[1]&&r[e["name"]]>t[1])}},f=function(e){Object(s["a"])(r,e);var t=Object(u["a"])(r);function r(){var e;Object(i["a"])(this,r);for(var n=arguments.length,a=new Array(n),c=0;c<n;c++)a[c]=arguments[c];return e=t.call.apply(t,[this].concat(a)),Object(l["a"])(Object(o["a"])(e),"data",[]),e}return Object(c["a"])(r,[{key:"queryAll",value:function(){this.loading=!0,this.filteredRawData=[];for(var e=0;e<this.rawData.length;e++){var t=this.rawData[e],r=!0;if(!Object(n["b"])(this.props.filter))for(var a=0;a<this.filterFields.length;a++)if(Object.prototype.hasOwnProperty.call(this.props.filter,this.fields[a]["name"])){var i=h[this.fields[a]["type"]||"equals"];if(!i(this.fields[a],this.props.filter[this.fields[a]["name"]],t)){r=!1;break}}if(r){if(Object(n["c"])(this.props.filter,"searchString")&&this.props.filter["searchString"])for(var c in r=!1,t)if(Object.prototype.hasOwnProperty.call(t,c))try{if(t[c].indexOf(this.props.filter["searchString"])>=0){r=!0;break}}catch(o){}r&&this.filteredRawData.push(t)}}return this.filteredRawData}},{key:"query",value:function(){this.queryAll();var e=this.props.itemsPerPage,t=this.props.page,r=(t-1)*e,n=r+e;this.rows=this.filteredRawData.slice(r,n),this.total=this.filteredRawData.length,this.loading=!1}},{key:"read",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"create",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"update",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()}]),r}(p),d=r("8e70"),m=function(e){Object(s["a"])(r,e);var t=Object(u["a"])(r);function r(){return Object(i["a"])(this,r),t.apply(this,arguments)}return Object(c["a"])(r,[{key:"getAll",value:function(){return null}},{key:"queryAll",value:function(){return null}},{key:"query",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(){var t,r,a,i;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return this.loading=!0,e.prev=1,r=this.props.itemsPerPage,a=this.props.page,i=Object(n["e"])({limit:r,page:a},this.props.filter),e.next=7,d["a"].get("/api/".concat(this.props.appName,"/").concat(this.props.objName,"/query"),{params:i});case 7:t=e.sent,this.rows=t.data.rows,this.total=(a-1)*r+this.rows.length+(this.rows.length<r?0:1),e.next=15;break;case 12:e.prev=12,e.t0=e["catch"](1),this.error=e.t0;case 15:this.loading=!1;case 16:case"end":return e.stop()}}),e,this,[[1,12]])})));function t(){return e.apply(this,arguments)}return t}()},{key:"read",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return this.loading=!0,e.prev=1,e.next=4,d["a"].get("/api/".concat(this.props.appName,"/").concat(this.props.objName,"/read"),{params:{id:t}});case 4:return r=e.sent,this.loading=!1,e.abrupt("return",r.data);case 7:return e.prev=7,this.loading=!1,e.finish(7);case 10:case"end":return e.stop()}}),e,this,[[1,,7,10]])})));function t(t){return e.apply(this,arguments)}return t}()},{key:"call",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return this.loading=!0,e.prev=1,e.next=4,d["a"].post("/api/".concat(this.props.appName,"/").concat(this.props.objName,"/").concat(t.method),t.data);case 4:return r=e.sent,this.loading=!1,e.abrupt("return",r.data);case 7:return e.prev=7,this.loading=!1,e.finish(7);case 10:case"end":return e.stop()}}),e,this,[[1,,7,10]])})));function t(t){return e.apply(this,arguments)}return t}()}]),r}(p),b=(r("e439"),r("5d41"),r("7e84"));function v(e,t){while(!Object.prototype.hasOwnProperty.call(e,t))if(e=Object(b["a"])(e),null===e)break;return e}function g(e,t,r){return g="undefined"!==typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=v(e,t);if(n){var a=Object.getOwnPropertyDescriptor(n,t);return a.get?a.get.call(r):a.value}},g(e,t,r||e)}var w=function(e){Object(s["a"])(r,e);var t=Object(u["a"])(r);function r(){var e;Object(i["a"])(this,r);for(var n=arguments.length,a=new Array(n),c=0;c<n;c++)a[c]=arguments[c];return e=t.call.apply(t,[this].concat(a)),Object(l["a"])(Object(o["a"])(e),"data",[]),e}return Object(c["a"])(r,[{key:"queryAll",value:function(){return this.rawData=this.store.getters["".concat(this.props["storeName"],"/getRawDataSource")](this.props.filter.operation||{},{root:!0})||[],g(Object(b["a"])(r.prototype),"queryAll",this).call(this)}},{key:"read",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"create",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"update",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:console.log(t);case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"call",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t.actionName="".concat(this.props.appName,"/").concat(this.props.objName,"/").concat(t.method),t.dataSource=this.props,e.next=4,this.store.dispatch("".concat(this.props.storeName,"/").concat(this.props.dispatchName),t,{root:!0});case 4:return e.abrupt("return",e.sent);case 5:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()}]),r}(f),y={Memory:f,Service:m,Vuex:w};function O(e,t){if(!Object(n["c"])(e,"type"))throw new Error("dataSource type not defined");if(Object(n["c"])(y,e["type"]))return new y[e["type"]](e,t);throw new Error("dataSource ".concat(e["type"]," not implemented"))}},b477:function(e,t,r){"use strict";var n=r("7577"),a=r.n(n);a.a}}]);
//# sourceMappingURL=chunk-12815540.7cd47f83.js.map