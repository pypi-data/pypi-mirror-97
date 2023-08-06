var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		if(__webpack_module_cache__[moduleId]) {
/******/ 			return __webpack_module_cache__[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_prop-types_index_js":"c8d76dec573b8ea6b9d0","vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js":"12640fcd7122c545b5c6","vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b":"fd6e5b36b7829d458f7a","vendors-node_modules_codemirror_lib_codemirror_js":"fb1f507032e0a2c2df89","vendors-node_modules_material-ui_core_esm_CssBaseline_CssBaseline_js-node_modules_material-ui-3f0525":"8b0ea3026a6f5770445e","vendors-node_modules_material-ui_core_styles_withStyles_js-node_modules_material-ui_icons_Che-bc3754":"7f45f3d005f929cbd1c0","webpack_sharing_consume_default_react":"245b7fa4c2367aab9882","webpack_sharing_consume_default_react-dom":"e31782e92a2e2e601172","lib_index_js":"ec8f941850d14b47d81b","vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-313cda":"c4826c33851ceb64e869","style_index_js":"041b07d05de08e3d3946","vendors-node_modules_material-ui_core_esm_ClickAwayListener_ClickAwayListener_js-node_modules-b27c83":"e22d4337c516a3c61827","vendors-node_modules_material-ui_core_esm_index_js":"84e2e711b1a1c3455fe3","vendors-node_modules_material-ui_icons_esm_index_js":"9c87a4128e83418d7202","node_modules_material-ui_core_esm_utils_createSvgIcon_js":"7f154fa0a2aae5409477","node_modules_stripe_stripe-js_dist_stripe_esm_js":"50ca52ea026ec3b498d1","vendors-node_modules_ansi-to-react_lib_index_js":"f6cbd666b734e46a1461","vendors-node_modules_moment_locale_af_js-node_modules_moment_locale_ar-dz_js-node_modules_mom-248d90":"f513836f7f99b632ba6c","node_modules_moment_locale_sync_recursive_":"80f733b6e3af688e351b","vendors-node_modules_notistack_dist_notistack_esm_js":"21483a64e4a4b37c85e1","vendors-node_modules_react-codemirror2_index_js":"a487cc5f5bd2c7cf059d","vendors-node_modules_react-linkify_dist_index_js":"38c7bb5eae933a42e80d","vendors-node_modules_micromark_dist_character_ascii-alpha_js-node_modules_micromark_dist_char-7c115a":"08c09f3ccaa61a1a6751","vendors-node_modules_react-markdown_lib_react-markdown_js":"7baa148f943fa04b277c","vendors-node_modules_remark-gfm_index_js":"62124ead821eece14882"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "jupyterlab_optumi:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/node module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.nmd = (module) => {
/******/ 			module.paths = [];
/******/ 			if (!module.children) module.children = [];
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "jupyterlab_optumi";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult.catch(handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@material-ui/core", "4.11.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_ClickAwayListener_ClickAwayListener_js-node_modules-b27c83"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_CssBaseline_CssBaseline_js-node_modules_material-ui-3f0525"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@material-ui/core/esm/index.js */ "./node_modules/@material-ui/core/esm/index.js"))))));
/******/ 					register("@material-ui/icons", "4.11.2", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_icons_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_material-ui_core_esm_utils_createSvgIcon_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/@material-ui/icons/esm/index.js */ "./node_modules/@material-ui/icons/esm/index.js"))))));
/******/ 					register("@stripe/stripe-js", "1.12.1", () => (__webpack_require__.e("node_modules_stripe_stripe-js_dist_stripe_esm_js").then(() => (() => (__webpack_require__(/*! ./node_modules/@stripe/stripe-js/dist/stripe.esm.js */ "./node_modules/@stripe/stripe-js/dist/stripe.esm.js"))))));
/******/ 					register("ansi-to-react", "6.1.4", () => (Promise.all([__webpack_require__.e("vendors-node_modules_ansi-to-react_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/ansi-to-react/lib/index.js */ "./node_modules/ansi-to-react/lib/index.js"))))));
/******/ 					register("jupyterlab_optumi", "3.4.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b"), __webpack_require__.e("vendors-node_modules_codemirror_lib_codemirror_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_CssBaseline_CssBaseline_js-node_modules_material-ui-3f0525"), __webpack_require__.e("vendors-node_modules_material-ui_core_styles_withStyles_js-node_modules_material-ui_icons_Che-bc3754"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("moment", "2.29.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_moment_locale_af_js-node_modules_moment_locale_ar-dz_js-node_modules_mom-248d90"), __webpack_require__.e("node_modules_moment_locale_sync_recursive_")]).then(() => (() => (__webpack_require__(/*! ./node_modules/moment/moment.js */ "./node_modules/moment/moment.js"))))));
/******/ 					register("notistack", "1.0.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_ClickAwayListener_ClickAwayListener_js-node_modules-b27c83"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b"), __webpack_require__.e("vendors-node_modules_notistack_dist_notistack_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom")]).then(() => (() => (__webpack_require__(/*! ./node_modules/notistack/dist/notistack.esm.js */ "./node_modules/notistack/dist/notistack.esm.js"))))));
/******/ 					register("react-codemirror2", "7.2.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_lib_codemirror_js"), __webpack_require__.e("vendors-node_modules_react-codemirror2_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-codemirror2/index.js */ "./node_modules/react-codemirror2/index.js"))))));
/******/ 					register("react-linkify", "1.0.0-alpha", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react-linkify_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-linkify/dist/index.js */ "./node_modules/react-linkify/dist/index.js"))))));
/******/ 					register("react-markdown", "5.0.3", () => (Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_micromark_dist_character_ascii-alpha_js-node_modules_micromark_dist_char-7c115a"), __webpack_require__.e("vendors-node_modules_react-markdown_lib_react-markdown_js"), __webpack_require__.e("webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-markdown/lib/react-markdown.js */ "./node_modules/react-markdown/lib/react-markdown.js"))))));
/******/ 					register("remark-gfm", "1.0.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_micromark_dist_character_ascii-alpha_js-node_modules_micromark_dist_char-7c115a"), __webpack_require__.e("vendors-node_modules_remark-gfm_index_js")]).then(() => (() => (__webpack_require__(/*! ./node_modules/remark-gfm/index.js */ "./node_modules/remark-gfm/index.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(1===range.length)return"*";if(0 in range){var r="",n=range[0];r+=0==n?">=":-1==n?"<":1==n?"^":2==n?"~":n>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,r+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return r}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,17,0,1])),
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersionCheck("default", "react-dom", [1,17,0,1])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application": () => (loadSingletonVersionCheck("default", "@jupyterlab/application", [1,3,0,4])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersionCheck("default", "@jupyterlab/services", [1,6,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docmanager": () => (loadSingletonVersionCheck("default", "@jupyterlab/docmanager", [1,3,0,4])),
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": () => (loadSingletonVersionCheck("default", "@lumino/coreutils", [1,1,5,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,3,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": () => (loadSingletonVersionCheck("default", "@jupyterlab/notebook", [1,3,0,4])),
/******/ 			"webpack/sharing/consume/default/@lumino/signaling": () => (loadSingletonVersionCheck("default", "@lumino/signaling", [1,1,4,3])),
/******/ 			"webpack/sharing/consume/default/@material-ui/core/@material-ui/core": () => (loadStrictVersionCheckFallback("default", "@material-ui/core", [1,4,11,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_material-ui_core_esm_ClickAwayListener_ClickAwayListener_js-node_modules-b27c83"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_index_js")]).then(() => (() => (__webpack_require__(/*! @material-ui/core */ "./node_modules/@material-ui/core/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": () => (loadSingletonVersionCheck("default", "@jupyterlab/ui-components", [1,3,0,3])),
/******/ 			"webpack/sharing/consume/default/react-codemirror2/react-codemirror2": () => (loadStrictVersionCheckFallback("default", "react-codemirror2", [1,7,2,1], () => (__webpack_require__.e("vendors-node_modules_react-codemirror2_index_js").then(() => (() => (__webpack_require__(/*! react-codemirror2 */ "./node_modules/react-codemirror2/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-markdown/react-markdown": () => (loadStrictVersionCheckFallback("default", "react-markdown", [1,5,0,3], () => (Promise.all([__webpack_require__.e("vendors-node_modules_micromark_dist_character_ascii-alpha_js-node_modules_micromark_dist_char-7c115a"), __webpack_require__.e("vendors-node_modules_react-markdown_lib_react-markdown_js")]).then(() => (() => (__webpack_require__(/*! react-markdown */ "./node_modules/react-markdown/lib/react-markdown.js"))))))),
/******/ 			"webpack/sharing/consume/default/remark-gfm/remark-gfm": () => (loadStrictVersionCheckFallback("default", "remark-gfm", [1,1,0,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_micromark_dist_character_ascii-alpha_js-node_modules_micromark_dist_char-7c115a"), __webpack_require__.e("vendors-node_modules_remark-gfm_index_js")]).then(() => (() => (__webpack_require__(/*! remark-gfm */ "./node_modules/remark-gfm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/ansi-to-react/ansi-to-react": () => (loadStrictVersionCheckFallback("default", "ansi-to-react", [1,6,0,8], () => (__webpack_require__.e("vendors-node_modules_ansi-to-react_lib_index_js").then(() => (() => (__webpack_require__(/*! ansi-to-react */ "./node_modules/ansi-to-react/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-linkify/react-linkify": () => (loadStrictVersionCheckFallback("default", "react-linkify", [1,1,0,0,,"alpha"], () => (__webpack_require__.e("vendors-node_modules_react-linkify_dist_index_js").then(() => (() => (__webpack_require__(/*! react-linkify */ "./node_modules/react-linkify/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/notistack/notistack": () => (loadStrictVersionCheckFallback("default", "notistack", [1,1,0,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_material-ui_core_esm_ClickAwayListener_ClickAwayListener_js-node_modules-b27c83"), __webpack_require__.e("vendors-node_modules_notistack_dist_notistack_esm_js")]).then(() => (() => (__webpack_require__(/*! notistack */ "./node_modules/notistack/dist/notistack.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@stripe/stripe-js/@stripe/stripe-js": () => (loadStrictVersionCheckFallback("default", "@stripe/stripe-js", [1,1,9,0], () => (__webpack_require__.e("node_modules_stripe_stripe-js_dist_stripe_esm_js").then(() => (() => (__webpack_require__(/*! @stripe/stripe-js */ "./node_modules/@stripe/stripe-js/dist/stripe.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@material-ui/icons/@material-ui/icons": () => (loadStrictVersionCheckFallback("default", "@material-ui/icons", [1,4,9,1], () => (__webpack_require__.e("vendors-node_modules_material-ui_icons_esm_index_js").then(() => (() => (__webpack_require__(/*! @material-ui/icons */ "./node_modules/@material-ui/icons/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/coreutils": () => (loadSingletonVersionCheck("default", "@jupyterlab/coreutils", [1,5,0,2])),
/******/ 			"webpack/sharing/consume/default/moment/moment": () => (loadStrictVersionCheckFallback("default", "moment", [1,2,29,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_moment_locale_af_js-node_modules_moment_locale_ar-dz_js-node_modules_mom-248d90"), __webpack_require__.e("node_modules_moment_locale_sync_recursive_")]).then(() => (() => (__webpack_require__(/*! moment */ "./node_modules/moment/moment.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docmanager",
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@lumino/signaling",
/******/ 				"webpack/sharing/consume/default/@material-ui/core/@material-ui/core",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/react-codemirror2/react-codemirror2",
/******/ 				"webpack/sharing/consume/default/react-markdown/react-markdown",
/******/ 				"webpack/sharing/consume/default/remark-gfm/remark-gfm",
/******/ 				"webpack/sharing/consume/default/ansi-to-react/ansi-to-react",
/******/ 				"webpack/sharing/consume/default/react-linkify/react-linkify",
/******/ 				"webpack/sharing/consume/default/notistack/notistack",
/******/ 				"webpack/sharing/consume/default/@stripe/stripe-js/@stripe/stripe-js",
/******/ 				"webpack/sharing/consume/default/@material-ui/icons/@material-ui/icons",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/coreutils",
/******/ 				"webpack/sharing/consume/default/moment/moment"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_modules__[id] = (module) => {
/******/ 							delete __webpack_module_cache__[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_modules__[id] = (module) => {
/******/ 							delete __webpack_module_cache__[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory).catch(onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// Promise = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"jupyterlab_optumi": 0
/******/ 		};
/******/ 		
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_react(|\-dom)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => {
/******/ 								installedChunkData = installedChunks[chunkId] = [resolve, reject];
/******/ 							});
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no deferred startup
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0, resolves = [];
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					resolves.push(installedChunks[chunkId][0]);
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 			for(moduleId in moreModules) {
/******/ 				if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 					__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 				}
/******/ 			}
/******/ 			if(runtime) runtime(__webpack_require__);
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			while(resolves.length) {
/******/ 				resolves.shift()();
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkjupyterlab_optumi"] = self["webpackChunkjupyterlab_optumi"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 		
/******/ 		// no deferred startup
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it uses a non-standard name for the exports (exports).
(() => {
var exports = __webpack_exports__;
/*!***********************!*\
  !*** container entry ***!
  \***********************/
var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b"), __webpack_require__.e("vendors-node_modules_codemirror_lib_codemirror_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_CssBaseline_CssBaseline_js-node_modules_material-ui-3f0525"), __webpack_require__.e("vendors-node_modules_material-ui_core_styles_withStyles_js-node_modules_material-ui_icons_Che-bc3754"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_prop-types_index_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_SvgIcon_SvgIcon_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_utils_debounce_js-node_modules_material-ui_core_esm-59045b"), __webpack_require__.e("vendors-node_modules_codemirror_lib_codemirror_js"), __webpack_require__.e("vendors-node_modules_material-ui_core_esm_CssBaseline_CssBaseline_js-node_modules_material-ui-3f0525"), __webpack_require__.e("vendors-node_modules_material-ui_core_styles_withStyles_js-node_modules_material-ui_icons_Che-bc3754"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./style": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-313cda"), __webpack_require__.e("style_index_js")]).then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var oldScope = __webpack_require__.S["default"];
	var name = "default"
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});
})();

(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).jupyterlab_optumi = __webpack_exports__;
/******/ })()
;
//# sourceMappingURL=remoteEntry.0e40470b4e15483ab94c.js.map