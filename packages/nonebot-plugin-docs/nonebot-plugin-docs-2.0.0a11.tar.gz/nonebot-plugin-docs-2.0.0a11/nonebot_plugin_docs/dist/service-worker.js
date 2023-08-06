/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a10/advanced/export-and-require.html",
    "revision": "e51aa3bd55d30c578b70d7e5e84e346c"
  },
  {
    "url": "2.0.0a10/advanced/index.html",
    "revision": "a9a6fa78faf7f853f07494c33946ed82"
  },
  {
    "url": "2.0.0a10/advanced/overloaded-handlers.html",
    "revision": "74e34162785d8f3b4d93d9d953b2caff"
  },
  {
    "url": "2.0.0a10/advanced/permission.html",
    "revision": "3595a3d0fa345b0005433f80a911bbcf"
  },
  {
    "url": "2.0.0a10/advanced/publish-plugin.html",
    "revision": "e10b2e89b1e4c94b7325456280ff6ef9"
  },
  {
    "url": "2.0.0a10/advanced/runtime-hook.html",
    "revision": "5f7c8c1b9c6b4d911acfac4d6139c0cb"
  },
  {
    "url": "2.0.0a10/advanced/scheduler.html",
    "revision": "b3645012a4badd3084528bb29048f4ca"
  },
  {
    "url": "2.0.0a10/api/adapters/cqhttp.html",
    "revision": "4978c1fbf31a83e76524f02333fca69f"
  },
  {
    "url": "2.0.0a10/api/adapters/ding.html",
    "revision": "746475ec28ed4b7359ef5f871eada52d"
  },
  {
    "url": "2.0.0a10/api/adapters/index.html",
    "revision": "a1eb9c0b51010d5db2c65f01ae51f739"
  },
  {
    "url": "2.0.0a10/api/adapters/mirai.html",
    "revision": "66bef8243658f621b8e36c748a5ccdf1"
  },
  {
    "url": "2.0.0a10/api/config.html",
    "revision": "2eaeb2841025879bbef7d946375ba5d3"
  },
  {
    "url": "2.0.0a10/api/drivers/fastapi.html",
    "revision": "8e35a007bdaa3d40dc4013fe95bad6ef"
  },
  {
    "url": "2.0.0a10/api/drivers/index.html",
    "revision": "eee499951c6a010556e2d45b86203762"
  },
  {
    "url": "2.0.0a10/api/drivers/quart.html",
    "revision": "36af6a43199cc2d4d55d356bac4b54cd"
  },
  {
    "url": "2.0.0a10/api/exception.html",
    "revision": "2613165a8d8e6e005cdbf0ce214e665d"
  },
  {
    "url": "2.0.0a10/api/index.html",
    "revision": "45448d22e1c43724d380568ad92a305d"
  },
  {
    "url": "2.0.0a10/api/log.html",
    "revision": "fc15c0c6ee199ee621420c6a427b4da7"
  },
  {
    "url": "2.0.0a10/api/matcher.html",
    "revision": "69c22ca383d82e0614d420587387eef2"
  },
  {
    "url": "2.0.0a10/api/message.html",
    "revision": "567e28d4acb910c5c28bf13349918ac2"
  },
  {
    "url": "2.0.0a10/api/nonebot.html",
    "revision": "42b346f1635d49e9714464ca386f82c1"
  },
  {
    "url": "2.0.0a10/api/permission.html",
    "revision": "e25f29389fa0cda56f9a98530c888503"
  },
  {
    "url": "2.0.0a10/api/plugin.html",
    "revision": "6c73ea1dd647aff0c0cc26189647411c"
  },
  {
    "url": "2.0.0a10/api/rule.html",
    "revision": "9016d97415b813be27451d7553c5368b"
  },
  {
    "url": "2.0.0a10/api/typing.html",
    "revision": "2768d4c9fa75a9a55ee0fd5c60418518"
  },
  {
    "url": "2.0.0a10/api/utils.html",
    "revision": "86fc59c1d442cf27baf225ca41ae1e99"
  },
  {
    "url": "2.0.0a10/guide/basic-configuration.html",
    "revision": "fc998dfa8825c77513cd14c0d9d1662e"
  },
  {
    "url": "2.0.0a10/guide/cqhttp-guide.html",
    "revision": "6e94bab3c168020ec9b70d80a2704119"
  },
  {
    "url": "2.0.0a10/guide/creating-a-handler.html",
    "revision": "37030345c6fda1e3b5b2e824814be263"
  },
  {
    "url": "2.0.0a10/guide/creating-a-matcher.html",
    "revision": "6bf7ed24cd6140391dbd5d0f3b01b06e"
  },
  {
    "url": "2.0.0a10/guide/creating-a-plugin.html",
    "revision": "0b67e7c953b5caf08b2e2aa8540e6b58"
  },
  {
    "url": "2.0.0a10/guide/creating-a-project.html",
    "revision": "99281af42c86f939bf6ad58b5e677b19"
  },
  {
    "url": "2.0.0a10/guide/ding-guide.html",
    "revision": "7f07ed8d525f3b30a3f52fecc603a4fe"
  },
  {
    "url": "2.0.0a10/guide/end-or-start.html",
    "revision": "70a9478ed5dbad8daf3733c4e05178eb"
  },
  {
    "url": "2.0.0a10/guide/getting-started.html",
    "revision": "31ff9c3583cd2ead491d86fc909ae7f7"
  },
  {
    "url": "2.0.0a10/guide/index.html",
    "revision": "0a82ac0cb2e257490d7edff622d04705"
  },
  {
    "url": "2.0.0a10/guide/installation.html",
    "revision": "c52948e095660f4bf6189c9fb3b5843f"
  },
  {
    "url": "2.0.0a10/guide/loading-a-plugin.html",
    "revision": "094933cb121aac64b641b11c789067d9"
  },
  {
    "url": "2.0.0a10/guide/mirai-guide.html",
    "revision": "c89fbada4ceb455e03c892196a358aba"
  },
  {
    "url": "2.0.0a10/index.html",
    "revision": "266dd00ac6c4df1951741d9568591de9"
  },
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "976328840940d42f89a277468ebeb090"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "b21572b09b0b30c83c6a5bee288b008e"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "3d704f50e944a21f6049f99e150282bf"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "e042df7fedbbcb60420b1cb4bb749ed5"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "66f367975504598fd137778e8833f3d3"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "f443f9428578ccda31792606f017e061"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "779f4b629db4e7e58f91e727273f70c2"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "735bbb1e5e18160957b6269da16e1f1d"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "620a3e40cc25a154b4676b5bdf43c624"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "0b22ca20e71e0a1313dbe45e8a54c273"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "ad659ef8d72d322dcf2257594c6aaf8c"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "1a0584794e1c378c8b0113f96a743910"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "11b84abe20bfc3917af09eb97757e84c"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "e2b14dbe0e44764740ff3bc8915c686d"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "5845701e18610c72d7e297d6ce1e15c4"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "e302bd6d57f372a89aa7c4d99a1b8d80"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "3e2cc0e059d524ee1476a7abdcd4a5f5"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "f88383cb134b630345504e7dd340932a"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "082b7cb8063d7d2a6ce8cba57caf6295"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "0efe6001c25541dfbad78103c4a83aa0"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "90e3cd0402823880908765825c6745e4"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "52249787934ca48c1baa24786a1f8c47"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "b8c46bf29561e149d11d9b8fc578bca6"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "c9a852bc8bfa4298c6dbd87d5220efb5"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "d68c7f118758b15a0f6fc3a94dda4d49"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "edd70e30a1a9097dcf5f0e6fdf9f3e0d"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "1d2e2b586ce26ce97c5056128d79d503"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "39bce5fa5cd99ab6fdb66def63934701"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "cb83792c24032a046f3baf46050bd8ac"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "cbbfc27058a5d254c50bde5c30e5c38d"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "e2e05ed20a714b8fdf8f12a76e9ffc43"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "b25cd6c51e012dead722cbc1487c6069"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "0bb43f112a3b3980be7a5d63fcb5d5ac"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "6b2eddb6cd76ac992796ff8238108d6a"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "dee0e50e1703245425657be563048d73"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "a2b91572c720760d581f971de68076fe"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "bbbfe088a90806aeed242d238caecb1c"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "0f55d9f976d62d53f19aef8d473a8e86"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "697b6021f8ae07773d0946943561d2c0"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "3bfa7a839a1a4f669529b3aa6b83281c"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "dfd669c675f126b35398d92b7eb5dc50"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "15354221645306f4786bc2ff1c566215"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "de40b1b948e046f1e8b408fdc965606a"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "2cb0f46818fadbbc7a1375e09d962d63"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "13d20d88fcd5142f61cedc2a25f78f09"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "fecb477d190bac6a31a4db4f1c0381ab"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "0941e927783778d16d8e7b2b03a28f2f"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "b2d49348371ad4d334ff9d72968e687d"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "6cfcb40fd944273e12d9efc2b2ee619c"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "3956d3b8e9f34fc13087fc37ee2c13ac"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "aa2d38e5db81b54a2fb4edb498587aa1"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "7002484cd2707ae3f05cef3d2c3441f2"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "329f835ca50d4fcdc0dd285f13b4347e"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "ab94694ee59e7f68d139ce3b9ac3f6dc"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "9a4355e991a511a61738061ab8a220fe"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "115841539a74613cc5a49f3e42c049ba"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "761bfd3f54971cfeaf27db8b3084a7f7"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "108cc249a6843369acbfe30bc37ef64a"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "93f32dbf0f0a998b93ac918c39e37e2d"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "d778fe78c3a9fe2509d725d88f312cce"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "883e69aad592c1e0811f089ccec985a8"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "4438a84cd3d9cce3329d4f55fbe7602a"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "aee2cd0b5b45f3aeb522a1faf68e37eb"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "b0e59b31d58e5918c7a5782451cf97b0"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "6346ffb83c34e78cf9413a3779fbfac8"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "7c7bd01f2cc139e3e30e18e603daa271"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "71b9953f8a762cc53fb9095cb4dfdfbe"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "28b8bcbcb3aee4517883ba76d35c3dcc"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "cbe29c8b7e7397fa651d22dbcc2f1608"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "1b6f713972798c1b09f6720fd691b921"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "beb58244f3dc2c135ff7c731112bcaf3"
  },
  {
    "url": "404.html",
    "revision": "ef276a72079c7f40e5aa6a4e930b39ed"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "87b8c5c8ffe8555638ae940dc185030f"
  },
  {
    "url": "advanced/index.html",
    "revision": "5a74f7289746b1839e1e47b8437c4232"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "6b4997f966897c54fde7d521a36d7330"
  },
  {
    "url": "advanced/permission.html",
    "revision": "a3e5998be5ffda1515073571451dc11e"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "9728cd73bf8575e99ae12ac8b3a93d93"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "bac358dbaa9f82c7b2693b861423efc5"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "0a48cede1f6a0f5430e302b0b60462ee"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "7a3852ec5372899393ecd2e9d5b6b714"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "2d18260e9337510cdb973097f5d18fb5"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "b47ffcecb5048941f76f5b7b771a3b76"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "99dc6060c605aebe283a36e72a34ed33"
  },
  {
    "url": "api/config.html",
    "revision": "b9796c40b12b18faa8783368d18c40e8"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "5c8df00c12eacbcbaef167e7bac7d57f"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "0cb4a696fc80ec47f4dad044c5949321"
  },
  {
    "url": "api/drivers/quart.html",
    "revision": "cfba7c841abd3439401e9a320c7cad03"
  },
  {
    "url": "api/exception.html",
    "revision": "dd383d950d5f7f06e35dd0abace07213"
  },
  {
    "url": "api/index.html",
    "revision": "c2d97413a345bac4af678f63348a48f2"
  },
  {
    "url": "api/log.html",
    "revision": "36256e9852ab22dcb131bbce5b90c14e"
  },
  {
    "url": "api/matcher.html",
    "revision": "aab06fcb56d05bfe0ea5394fc6198b71"
  },
  {
    "url": "api/message.html",
    "revision": "705023df06884802dde8924cfbabaa5a"
  },
  {
    "url": "api/nonebot.html",
    "revision": "5e6624fc630143893a607cfc4727908f"
  },
  {
    "url": "api/permission.html",
    "revision": "0faf86ec691e810d505d12464b769904"
  },
  {
    "url": "api/plugin.html",
    "revision": "cbe9beff12d6384ee505f22c902b5a91"
  },
  {
    "url": "api/rule.html",
    "revision": "8d682369ce4901bd098bb7ac6bd24eb3"
  },
  {
    "url": "api/typing.html",
    "revision": "3a5a489f11f4dbd9f6a9c42956e1aaef"
  },
  {
    "url": "api/utils.html",
    "revision": "66a045f5d51241ed2c9cd85a4900c7fb"
  },
  {
    "url": "assets/css/0.styles.6f30ed4c.css",
    "revision": "f035baf5b517bd58f11dca881ce3ff23"
  },
  {
    "url": "assets/img/Handle-Event.1e964e39.png",
    "revision": "1e964e39a1e302bc36072da2ffe9f509"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.534daa54.js",
    "revision": "3ea50aebcc9695f85d56fdd13bc9c7ce"
  },
  {
    "url": "assets/js/100.365eb65a.js",
    "revision": "e601fbbc8ae718f5ac9aa89fad7e5177"
  },
  {
    "url": "assets/js/101.59f9cb56.js",
    "revision": "f59432d57bc3c7b9e5b47eabc4f42346"
  },
  {
    "url": "assets/js/102.eb7c7374.js",
    "revision": "01a33947d962fe984d20bca458110edd"
  },
  {
    "url": "assets/js/103.484fca0c.js",
    "revision": "48a7c2a3988ece6572028119063bf784"
  },
  {
    "url": "assets/js/104.cb8cc75b.js",
    "revision": "2a375edfcc52901c03ca83e7afa465c8"
  },
  {
    "url": "assets/js/105.425c1ea7.js",
    "revision": "422278929f0c9aba557ec5939ac3992f"
  },
  {
    "url": "assets/js/106.d19965d0.js",
    "revision": "d259d618b3c0dc4d15b96163b0f47159"
  },
  {
    "url": "assets/js/107.ce220a8d.js",
    "revision": "acd811130c713f2bf208aa07a37abe8f"
  },
  {
    "url": "assets/js/108.7d5ed38a.js",
    "revision": "8df55ca0b0ec5d3746fe7d81b79be51b"
  },
  {
    "url": "assets/js/109.5f12d061.js",
    "revision": "3aaa05a348e5ddcd8fb485ac4ca2898d"
  },
  {
    "url": "assets/js/11.fb4f86e6.js",
    "revision": "9ba59461103d1661b266a98295d6088c"
  },
  {
    "url": "assets/js/110.6cd05411.js",
    "revision": "a44b0bf4bd43c4a177b57eec84c36279"
  },
  {
    "url": "assets/js/111.76ac5b3e.js",
    "revision": "8f0b72ea15681a968309cb6c269bb86f"
  },
  {
    "url": "assets/js/112.09b2b578.js",
    "revision": "da300bc2a4dde5e6b83160cdefd30e27"
  },
  {
    "url": "assets/js/113.d1c27189.js",
    "revision": "635106291728b56aa833c9e5737a8eca"
  },
  {
    "url": "assets/js/114.ba64ab4c.js",
    "revision": "60009d94bdcc5dad05ebf491afeddbde"
  },
  {
    "url": "assets/js/115.ee8bb7a5.js",
    "revision": "6fd31184856e4f037244e7e12333186b"
  },
  {
    "url": "assets/js/116.c8d0e1b4.js",
    "revision": "64920de2da0ef1e34374de4336cacd7f"
  },
  {
    "url": "assets/js/117.01c43e11.js",
    "revision": "571e22ba3388446729c4085563feff82"
  },
  {
    "url": "assets/js/118.4ab94b6c.js",
    "revision": "dbb9415d3d9a5ff6f15a26ec86545beb"
  },
  {
    "url": "assets/js/119.0a494730.js",
    "revision": "ae14ec945e5f9ec3604f7749c65ebebf"
  },
  {
    "url": "assets/js/12.a58e4354.js",
    "revision": "51badfed498fbe6f9bb143a0d7911ae3"
  },
  {
    "url": "assets/js/120.f09a06ed.js",
    "revision": "ee4854a843381a26509b314f29f2ef2f"
  },
  {
    "url": "assets/js/121.325322cd.js",
    "revision": "d5e2e7694d26d242a7a7bb373c55d46d"
  },
  {
    "url": "assets/js/122.b344b5fd.js",
    "revision": "91365ad3f10331e8b47da0d4c415a420"
  },
  {
    "url": "assets/js/123.71c2b610.js",
    "revision": "523947a043ba35918e8d5a9778c9ffb7"
  },
  {
    "url": "assets/js/124.495d4397.js",
    "revision": "2ee6fbbe67a0375e356f75587ddbd557"
  },
  {
    "url": "assets/js/125.c3fcc326.js",
    "revision": "dbe802807132ebff01e472a86b9da2e0"
  },
  {
    "url": "assets/js/126.31d8c302.js",
    "revision": "4e3369795cea2d0da2df6a0480a4f0ed"
  },
  {
    "url": "assets/js/127.55b8e3db.js",
    "revision": "d0962719114405a2d1b449041c32b7c6"
  },
  {
    "url": "assets/js/128.a7be93c6.js",
    "revision": "bf202adaab6ac1c7a27eb707735b4975"
  },
  {
    "url": "assets/js/129.2880d060.js",
    "revision": "c0b30e5842ce01ee1ddd36ad79706fcd"
  },
  {
    "url": "assets/js/13.ef65eb21.js",
    "revision": "611d12cbc87efe8f21a023ad2184a468"
  },
  {
    "url": "assets/js/130.3563b8ac.js",
    "revision": "29c286c0e9e788cc7b98fb1fa875d90c"
  },
  {
    "url": "assets/js/131.5c1a0666.js",
    "revision": "1b3a80d2f62e451f9bf97cd10136e747"
  },
  {
    "url": "assets/js/132.50b7ca01.js",
    "revision": "11267aa4ea8c5a7a4732c0ea896aeb9a"
  },
  {
    "url": "assets/js/133.364b80ee.js",
    "revision": "0a75ab89e55dfc1e85f0c907481171fb"
  },
  {
    "url": "assets/js/134.568bb6c4.js",
    "revision": "65e49d17660e8eae3f8c02df8886b551"
  },
  {
    "url": "assets/js/135.c5c50485.js",
    "revision": "e5a382065cac4ea5d5eac85cb69e9183"
  },
  {
    "url": "assets/js/136.7aa09f7c.js",
    "revision": "4ae43c581c6ed962b85df3211a9020b7"
  },
  {
    "url": "assets/js/137.d6178918.js",
    "revision": "52a6f646b59d4c62083ae8cfd10adc53"
  },
  {
    "url": "assets/js/138.098ad709.js",
    "revision": "bf70229e1900afe5e937f0e3aa33a92c"
  },
  {
    "url": "assets/js/139.636ce292.js",
    "revision": "840b50e9dca47b60dc8d32ec8aa3f890"
  },
  {
    "url": "assets/js/14.56bfcd00.js",
    "revision": "3a3521b6d83acfd7a5979956816ed770"
  },
  {
    "url": "assets/js/140.4fc47057.js",
    "revision": "389bc12a692d6e862814b84978c6869d"
  },
  {
    "url": "assets/js/141.3fc83ebf.js",
    "revision": "0b34f095b5bd45d2bbb8d940d4c158da"
  },
  {
    "url": "assets/js/142.f15840f3.js",
    "revision": "7c44ac7b4b4537e47280f091146fb129"
  },
  {
    "url": "assets/js/143.dd4eb6ac.js",
    "revision": "b0eddd4923b964962122d77d9c5042b5"
  },
  {
    "url": "assets/js/144.3d05828e.js",
    "revision": "9cd6cbd9ee701c6f747b86bbed864004"
  },
  {
    "url": "assets/js/145.c1407409.js",
    "revision": "4d00345eadbc3f9b492c387de590b00f"
  },
  {
    "url": "assets/js/146.e190dd33.js",
    "revision": "e45c11b8e9bfd6e2eb810fa83071b208"
  },
  {
    "url": "assets/js/147.93935ec2.js",
    "revision": "e90b0abeb91a3751a5c86606de261cd0"
  },
  {
    "url": "assets/js/148.eb230a4e.js",
    "revision": "1d22890f3dfe2562c70a946b2280066f"
  },
  {
    "url": "assets/js/149.8d0ece1f.js",
    "revision": "070ebe71b095ef87bcb28bbe2cfa6619"
  },
  {
    "url": "assets/js/15.12eb8876.js",
    "revision": "a6d711b6e069c02ca2dfdfb12ec59a68"
  },
  {
    "url": "assets/js/150.a7a873a1.js",
    "revision": "f3c1690289e75bb7ff84f369d59ef963"
  },
  {
    "url": "assets/js/151.bbc71288.js",
    "revision": "2f052ebbf1661a6f9d1eb105c2d99e6b"
  },
  {
    "url": "assets/js/152.224343b1.js",
    "revision": "47183aaf14e6965aa926adb4f2664a84"
  },
  {
    "url": "assets/js/153.7df26699.js",
    "revision": "e3fde7f5e55a414d1ab1d0f891a383f4"
  },
  {
    "url": "assets/js/154.851e4481.js",
    "revision": "7a582e6837bef05296b02471f8988851"
  },
  {
    "url": "assets/js/155.e47c6c90.js",
    "revision": "4d94aa3cbaa65be5c3b965b087295f03"
  },
  {
    "url": "assets/js/156.f09d42a4.js",
    "revision": "0a2213f6c0cc6586c9188f079c4f8241"
  },
  {
    "url": "assets/js/157.74bd047e.js",
    "revision": "f4d7f509db597e5c912cfcd6a06fc4f5"
  },
  {
    "url": "assets/js/158.bad14f21.js",
    "revision": "41d959ca7ab8786c86f50d3c39a18bba"
  },
  {
    "url": "assets/js/159.39ec4155.js",
    "revision": "76269f295dc7fce4193c8ec91b6128de"
  },
  {
    "url": "assets/js/16.a0669648.js",
    "revision": "9e6039fcb3c53a0f03615e0913945078"
  },
  {
    "url": "assets/js/160.4c7d25f9.js",
    "revision": "66af7bee015a719769a9a4d7f554c8ae"
  },
  {
    "url": "assets/js/161.e8dfcd85.js",
    "revision": "36edb506d47e4ca2d83faa94ba1ddbd8"
  },
  {
    "url": "assets/js/162.75c7d882.js",
    "revision": "4582067a2bae6d2ab45dd8d94ee81d3a"
  },
  {
    "url": "assets/js/163.57027f73.js",
    "revision": "86538e4c755f6154f9182c80b05af9aa"
  },
  {
    "url": "assets/js/164.a00d89bd.js",
    "revision": "69d83606c18c3ef743fb9c0a51ebf8ec"
  },
  {
    "url": "assets/js/165.976bfb04.js",
    "revision": "9c6bd051bf5a7654a79fe69f5fc201ed"
  },
  {
    "url": "assets/js/166.8dc64119.js",
    "revision": "20a8cab9b6b5d5eed00925d3d0f1d7f4"
  },
  {
    "url": "assets/js/167.97cfe52d.js",
    "revision": "92fb3299387ba09d069c86971ee876b4"
  },
  {
    "url": "assets/js/168.3f131423.js",
    "revision": "a2c0bec1d00d93a00fd83868ac16909e"
  },
  {
    "url": "assets/js/169.46e33c8d.js",
    "revision": "ccd0d75502dc525062bfc8bca49005f7"
  },
  {
    "url": "assets/js/17.ef6c0687.js",
    "revision": "210b2d59aad06f125189e010d5ada734"
  },
  {
    "url": "assets/js/170.782db1e5.js",
    "revision": "de2e4a64417897e58864e534eae556b8"
  },
  {
    "url": "assets/js/171.5794f4ad.js",
    "revision": "092b014971e26ca48331a0714327f19d"
  },
  {
    "url": "assets/js/172.e917f612.js",
    "revision": "3efe665add9407bae0c3cd0fc3b4382a"
  },
  {
    "url": "assets/js/173.4afdaffb.js",
    "revision": "88a7c4c03ace3b18aacaec3c9c402534"
  },
  {
    "url": "assets/js/174.a5f23675.js",
    "revision": "986a3b98073e13182da6e69dc39984b0"
  },
  {
    "url": "assets/js/175.a49c4ab2.js",
    "revision": "84b86ff4511e3aad3a29b58226143efd"
  },
  {
    "url": "assets/js/176.ba298fc6.js",
    "revision": "7eb335d0618fe66d0831337488db7349"
  },
  {
    "url": "assets/js/177.05c07aef.js",
    "revision": "45893a67886eb1c2eefc729a5fa986d9"
  },
  {
    "url": "assets/js/178.845c4bbc.js",
    "revision": "3c7bbe5755a2c7e3ed46a4a5557d7de1"
  },
  {
    "url": "assets/js/179.863eae4a.js",
    "revision": "893ec3ff643bdad0c9dc3b56c66557fc"
  },
  {
    "url": "assets/js/18.89318948.js",
    "revision": "cb7ff50c9469c0c684367883e5796200"
  },
  {
    "url": "assets/js/180.ffb7dfce.js",
    "revision": "27f8bd8929a57996e533cf4f0d0d7bbe"
  },
  {
    "url": "assets/js/181.d9c552d9.js",
    "revision": "73022d572f5d41f68c8407fb10981c14"
  },
  {
    "url": "assets/js/182.8d5b9c24.js",
    "revision": "c741dab7bab66c5dc75857fda39c9558"
  },
  {
    "url": "assets/js/183.da765cd4.js",
    "revision": "625dc3090551933bb559c040ab2266a7"
  },
  {
    "url": "assets/js/184.2618c788.js",
    "revision": "7a8f63f728e1e96c379fca717dd817a7"
  },
  {
    "url": "assets/js/185.9678222c.js",
    "revision": "dac29a8b8088efd2c6f8f37fb38ca4c4"
  },
  {
    "url": "assets/js/186.b3eb737f.js",
    "revision": "cf435d3bb24ebf30e900acb31f338094"
  },
  {
    "url": "assets/js/187.e8240d96.js",
    "revision": "7741273638f7b4c8926f14268090d82b"
  },
  {
    "url": "assets/js/188.6d5e5537.js",
    "revision": "98670cf6504a0bc84918a77ca2e508f6"
  },
  {
    "url": "assets/js/189.9a61a235.js",
    "revision": "5fffbbdb8d40322cb3789f2398b4b1c0"
  },
  {
    "url": "assets/js/19.df56cb76.js",
    "revision": "8f033412e8b69ad5359712a6c71fb0ea"
  },
  {
    "url": "assets/js/190.21a348f2.js",
    "revision": "6e51c8db3b3f142dccc50e02fabe8edc"
  },
  {
    "url": "assets/js/191.f4b3e1e8.js",
    "revision": "acc2e890e18f50dbb5566b76b0b27f51"
  },
  {
    "url": "assets/js/192.1a131d48.js",
    "revision": "ff74b60d9d3a9cc32d87a1fb1a4a60de"
  },
  {
    "url": "assets/js/193.af51fe58.js",
    "revision": "8fd15c61911f1ac39bd800e2297cc333"
  },
  {
    "url": "assets/js/194.d54d3f37.js",
    "revision": "9477b51d1604b0e8604d9f9902713989"
  },
  {
    "url": "assets/js/195.fe4dd95e.js",
    "revision": "e8bf1247bf9b54b8ea835ce0573bf514"
  },
  {
    "url": "assets/js/196.449ef11a.js",
    "revision": "007d3a65859897172f64d2f7e27e6d4b"
  },
  {
    "url": "assets/js/197.7785a626.js",
    "revision": "048b1d0b3fb76ba2f163b3ab55674347"
  },
  {
    "url": "assets/js/198.04857bb9.js",
    "revision": "0c9419fa6818374bdee87bdd3c77940b"
  },
  {
    "url": "assets/js/199.4fe6e3a6.js",
    "revision": "6859f8e310cb5b48d1722915304d071b"
  },
  {
    "url": "assets/js/2.fbe1c23f.js",
    "revision": "d0c12e3731c81a6a7a794aa59ddc7d12"
  },
  {
    "url": "assets/js/20.867259fb.js",
    "revision": "c6a88e115da18773678ee0b7132338fa"
  },
  {
    "url": "assets/js/200.bde436c1.js",
    "revision": "f63dca6399c3e0d4e659d93938244f92"
  },
  {
    "url": "assets/js/201.3d43db63.js",
    "revision": "9928fde5bd9ae9f60f8b8ecb30422626"
  },
  {
    "url": "assets/js/202.2fab4d99.js",
    "revision": "95c3a11a3e0d66a04ac97c1e8f0a180c"
  },
  {
    "url": "assets/js/203.65dff636.js",
    "revision": "a127290df79883954310f51751e8db2c"
  },
  {
    "url": "assets/js/204.484e0d60.js",
    "revision": "4d9bc6e881fbfa24b748d0cda5bb6cb7"
  },
  {
    "url": "assets/js/205.07f2a43e.js",
    "revision": "5ba6049e3006e055b2d8c3f7c0cd896e"
  },
  {
    "url": "assets/js/206.4e4cd4e0.js",
    "revision": "5158efdd5aa93b380c531b2e59bf223b"
  },
  {
    "url": "assets/js/21.c2bd2832.js",
    "revision": "a96bf42366df7631940bdc95f9281f2f"
  },
  {
    "url": "assets/js/22.eb9df317.js",
    "revision": "ec3b1f47e7404c132573dd5d2ea6061a"
  },
  {
    "url": "assets/js/23.104b2c07.js",
    "revision": "f0ed1bad5a9d9c04462b2803ca61e266"
  },
  {
    "url": "assets/js/24.6a35437a.js",
    "revision": "e1c5630e03f171ef9d873993dfea23cc"
  },
  {
    "url": "assets/js/25.5d6d9bd2.js",
    "revision": "5dc03415d43792a7eef559a23927f201"
  },
  {
    "url": "assets/js/26.c60cf300.js",
    "revision": "ce9d0e9bf2f11e73bcac1105698c97c8"
  },
  {
    "url": "assets/js/27.37585ed5.js",
    "revision": "9e45513dd831862a43a47c04230027b8"
  },
  {
    "url": "assets/js/28.f23c2b72.js",
    "revision": "647ecae12658f4d431b6f209372430d1"
  },
  {
    "url": "assets/js/29.06ccb8e8.js",
    "revision": "cc4f6983a3288c769acf579ed228fac0"
  },
  {
    "url": "assets/js/3.818c639d.js",
    "revision": "2681cd4fb3edc8e0b6d0e0f265585ce8"
  },
  {
    "url": "assets/js/30.1c638732.js",
    "revision": "c0e8d7cc45c0a4b24778d5a2689a26b0"
  },
  {
    "url": "assets/js/31.ca0b1d56.js",
    "revision": "5b9b39d144c893040a364cf44342c827"
  },
  {
    "url": "assets/js/32.696de254.js",
    "revision": "80298900325c56268a2dbcef5c46528d"
  },
  {
    "url": "assets/js/33.31ca2fdd.js",
    "revision": "77b3003f5ba4e16e7373b3c7e3bb5873"
  },
  {
    "url": "assets/js/34.a9ea47fd.js",
    "revision": "24ab76ec4ea5f04d426ddd3457b32453"
  },
  {
    "url": "assets/js/35.e8e40a5d.js",
    "revision": "4659b00fe971db4b570acd314f29196e"
  },
  {
    "url": "assets/js/36.d2a458ed.js",
    "revision": "7c5c370b1b006ee47bb69f9cce5e6c8d"
  },
  {
    "url": "assets/js/37.33580414.js",
    "revision": "42b03888845220d33448f3ea10253792"
  },
  {
    "url": "assets/js/38.4bd30882.js",
    "revision": "d47078392066587114e121ec983f0479"
  },
  {
    "url": "assets/js/39.9c8236d4.js",
    "revision": "616d1f74543cd340b7e9972204d5db76"
  },
  {
    "url": "assets/js/4.482e9ad9.js",
    "revision": "0c48c4c7c30ca4df6c9068a568eda98f"
  },
  {
    "url": "assets/js/40.ff16e7c6.js",
    "revision": "ad2c654eb4c62200de1acf980eca9212"
  },
  {
    "url": "assets/js/41.94e901b0.js",
    "revision": "b9601db25e28801bdd70e65227dbb420"
  },
  {
    "url": "assets/js/42.36124ecd.js",
    "revision": "2f8fa536b11f3f3c56e96d2038e3689f"
  },
  {
    "url": "assets/js/43.1c10346d.js",
    "revision": "e40027cb7a74c979205461cd4278caa9"
  },
  {
    "url": "assets/js/44.6cf59049.js",
    "revision": "687d8fb65b832170f0314809908e8043"
  },
  {
    "url": "assets/js/45.150f7059.js",
    "revision": "7145459734271f3a71f7dfbfc4deedb9"
  },
  {
    "url": "assets/js/46.41c824bc.js",
    "revision": "3392b3785e5e85fe94e35bf5167aef86"
  },
  {
    "url": "assets/js/47.2c6122e4.js",
    "revision": "a15a781c1342c52c206767129bc86cca"
  },
  {
    "url": "assets/js/48.cb07f0b1.js",
    "revision": "8865c1741b4841a106f2372e78807e09"
  },
  {
    "url": "assets/js/49.87b0284c.js",
    "revision": "16c3789ce14a2a21b29a9f08ee141883"
  },
  {
    "url": "assets/js/5.f2c02d46.js",
    "revision": "dc4ba53762828f8118f50e31b758ee25"
  },
  {
    "url": "assets/js/50.97a2ca1e.js",
    "revision": "753e5fdecb5b38499a7060c708869ae6"
  },
  {
    "url": "assets/js/51.2062cb12.js",
    "revision": "e28c077c2e05a8846ae7b7a297a27439"
  },
  {
    "url": "assets/js/52.1d3a0c21.js",
    "revision": "dd837b14fc2090c3a824dbc155f2f467"
  },
  {
    "url": "assets/js/53.6157dbd2.js",
    "revision": "e03d43a65446aad6602dca4704da901c"
  },
  {
    "url": "assets/js/54.cc92576c.js",
    "revision": "fd91f37622a00570ba43f1acc24136c8"
  },
  {
    "url": "assets/js/55.c311de7c.js",
    "revision": "f38163d9a5e0e449f23af129da19f4d1"
  },
  {
    "url": "assets/js/56.7a0b2d92.js",
    "revision": "b226b3651d576bbdf86881a6c4d97c4f"
  },
  {
    "url": "assets/js/57.c89d1d4a.js",
    "revision": "0c7b055c3612bf599eadc920c1abcde2"
  },
  {
    "url": "assets/js/58.06a00d47.js",
    "revision": "7c58e1dfc9237339098a07807f356e1f"
  },
  {
    "url": "assets/js/59.13cee857.js",
    "revision": "7ff55d34e58bac36ed214e5b73ae92d3"
  },
  {
    "url": "assets/js/6.feb8d29a.js",
    "revision": "32611d93dee96633266721acdff37e1b"
  },
  {
    "url": "assets/js/60.64044861.js",
    "revision": "5acfe00f556ce7028aff0d04997d07ed"
  },
  {
    "url": "assets/js/61.2c37338a.js",
    "revision": "409e4feb08d4d732bcd68d0d3edd85cf"
  },
  {
    "url": "assets/js/62.667cdd34.js",
    "revision": "dcdf5c637fd75ac82baa6e78b43b69b2"
  },
  {
    "url": "assets/js/63.429196b5.js",
    "revision": "7323d14ce8da8a3a9874097cdabe5375"
  },
  {
    "url": "assets/js/64.5bf797a8.js",
    "revision": "207f4e91a157ccfdac81b254148d2e3c"
  },
  {
    "url": "assets/js/65.a28cac3f.js",
    "revision": "746d42a5e9259149ccc896496eee9616"
  },
  {
    "url": "assets/js/66.8b7e3beb.js",
    "revision": "69633ff4da0428b4f853c68fdf725354"
  },
  {
    "url": "assets/js/67.b033909c.js",
    "revision": "c7cf8c1d409b21ecf729413910302f98"
  },
  {
    "url": "assets/js/68.ee54dc32.js",
    "revision": "52fbf5a81677afe33eb1862e83c40e8f"
  },
  {
    "url": "assets/js/69.ed957a83.js",
    "revision": "e712f05b2f5373f5ef4a4b7fcce29a85"
  },
  {
    "url": "assets/js/7.516d9a34.js",
    "revision": "cf25387a229da0d20e25bbcaa494a04c"
  },
  {
    "url": "assets/js/70.05608313.js",
    "revision": "a16e98b2c2f87536dd944d1d66785dfd"
  },
  {
    "url": "assets/js/71.39f887e1.js",
    "revision": "d3e6da624ebbad6240cc1fff42783294"
  },
  {
    "url": "assets/js/72.926d14f9.js",
    "revision": "c5b925bdb0b603c551df5245718e01bb"
  },
  {
    "url": "assets/js/73.7498927e.js",
    "revision": "5af27b6e451d2a17c8bef348cff9f235"
  },
  {
    "url": "assets/js/74.ce94047b.js",
    "revision": "77b5b91556035f3103d82b4cd7bd0ab4"
  },
  {
    "url": "assets/js/75.9cc5f903.js",
    "revision": "086fab15e877bb890730afc34fbf36a0"
  },
  {
    "url": "assets/js/76.14796ee8.js",
    "revision": "d50e40ce31e468c445f37036527fdbe9"
  },
  {
    "url": "assets/js/77.124c7a56.js",
    "revision": "5c07467290336f44c38731e801cd7888"
  },
  {
    "url": "assets/js/78.b2d2b690.js",
    "revision": "75771728008b066e2ee54ebeb1ec5d8d"
  },
  {
    "url": "assets/js/79.bd67d7dc.js",
    "revision": "147212ece44326e036d6d85b6874890a"
  },
  {
    "url": "assets/js/8.fcaab402.js",
    "revision": "1ddca6d0984d0c515d7965b28e66073b"
  },
  {
    "url": "assets/js/80.b4dcf9b1.js",
    "revision": "ebef50515635e64bbd761998eac51cbe"
  },
  {
    "url": "assets/js/81.a204da04.js",
    "revision": "16b10471ca3d76762feaeb7e6dbad25c"
  },
  {
    "url": "assets/js/82.51f6177c.js",
    "revision": "b7a9f571254dbfe9318d6896cd6ceaca"
  },
  {
    "url": "assets/js/83.22fdd3f2.js",
    "revision": "78612cb4de23c06e0b9cc387b77a2727"
  },
  {
    "url": "assets/js/84.d895c979.js",
    "revision": "cd32ab24e49d29749f50e410ddf41fdd"
  },
  {
    "url": "assets/js/85.afac344a.js",
    "revision": "92ca19c6be6c0fd111a177ffded6d524"
  },
  {
    "url": "assets/js/86.2299c062.js",
    "revision": "5fc55928d029bf5243d9f11e3acda3da"
  },
  {
    "url": "assets/js/87.1a01f41c.js",
    "revision": "e2a03b86ef55378b62bbee16955aca02"
  },
  {
    "url": "assets/js/88.7d8a7541.js",
    "revision": "f068dc275a57724aa9e4b750cc005343"
  },
  {
    "url": "assets/js/89.d8bc242f.js",
    "revision": "62237a33b2dd447d67becfd7385cb99c"
  },
  {
    "url": "assets/js/9.a7305841.js",
    "revision": "c7bb66311cfb10cde2c7ccedd2b4b17e"
  },
  {
    "url": "assets/js/90.8fd26ec4.js",
    "revision": "0fd39fa67cda347cc79401a0c2a82bdf"
  },
  {
    "url": "assets/js/91.de63a0ac.js",
    "revision": "9909b47fac96b927c9fc9c92478f908f"
  },
  {
    "url": "assets/js/92.214f82d1.js",
    "revision": "f76e96691072401d3af378ac219ebbde"
  },
  {
    "url": "assets/js/93.36b59f38.js",
    "revision": "c3475ea82e57752099424b62f1bc51f9"
  },
  {
    "url": "assets/js/94.dce1ff6b.js",
    "revision": "ffdc345d7775f9090cbd9bf9453bb1aa"
  },
  {
    "url": "assets/js/95.aedfd0a9.js",
    "revision": "be329d7b5dd37b4b4f568adbddd10280"
  },
  {
    "url": "assets/js/96.f8623b22.js",
    "revision": "c3dc876056029bbe7a8f9395b43bc8ee"
  },
  {
    "url": "assets/js/97.9a0d583c.js",
    "revision": "20f69de1755ab74909d210781ad9225c"
  },
  {
    "url": "assets/js/98.eb35514a.js",
    "revision": "c3f3d33bd4003189d315531dd45d30fd"
  },
  {
    "url": "assets/js/99.078cc580.js",
    "revision": "e3a529d95d4fb5c06fd0e49948677336"
  },
  {
    "url": "assets/js/app.4b4a560c.js",
    "revision": "4facb532bd751972389549d47aaad6d9"
  },
  {
    "url": "changelog.html",
    "revision": "1ea44b6b17e200bc7a62b6199776eec5"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "2b3ed44538d64905d50c027590a0f958"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "24f74523e2751e33c4439081100114ae"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "f53d5969c21a223b4d6478dacd1735ca"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "92a94ca70d8b200c64b552431c000ac1"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "1fa418513e71dc9723e73baacac2cb83"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "da5afb51f9dc66b413c02c6e7cbb0d86"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "0f120a5fe26014abed16ca2be62d840c"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "57a15e192364ff3ad217cfcf7934c373"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "2b5ac644ce9de4910ae319a6d70880f6"
  },
  {
    "url": "guide/index.html",
    "revision": "f0d8d1ab05803e687b514a9239f66b78"
  },
  {
    "url": "guide/installation.html",
    "revision": "33882b00ae3cdf336358f32c8e36f40e"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "80e48ee299e400b9e4048ac1178174a6"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "6e8e357dc570a185f5f5b34ae462d56f"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "dfcb3c73d13a28456db99603f91ec198"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "03e5b9e6e87be7be82283c5e06536c16"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "1857a065a2b84537bfaa7683c35add9c"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "5c45a35ae146c99b9ce93293c6516160"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "359527c60717996c8868efc6487c5512"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "bbba5a80f232e1d70c51099484afb31b"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "33033fc9926733c5bc8c6514f4a2b39c"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "c49920022bf6f06355ad3fec8ed86a8d"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "b0311af758091f336f7f95499ab4ecf7"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "db8c7887d86db65fbeed860b9e31860d"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "d68b577dca4f900f7539877124282ee7"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "a50cc27e30ee5f05e324971aff461a3b"
  },
  {
    "url": "next/api/config.html",
    "revision": "a0b2342351a58f75f36b9a30246f6481"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "8fb909a8d907148e306166523b2c5ab7"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "e92529e001a40f7ce09db7dbdd7d88e4"
  },
  {
    "url": "next/api/drivers/quart.html",
    "revision": "493c0e054a81236208bc8cc8ed58de33"
  },
  {
    "url": "next/api/exception.html",
    "revision": "29d410c6df2e30add384d3c6ccbb504d"
  },
  {
    "url": "next/api/index.html",
    "revision": "32d603317985277d30e8998697543e37"
  },
  {
    "url": "next/api/log.html",
    "revision": "b62191aa04ef9f316505a1a5a558e39b"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "ded09bbde3848bef1428522c2a8f4717"
  },
  {
    "url": "next/api/message.html",
    "revision": "e8633c81a997c156a2a20a0601d04065"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "9f27144586e411c7a576ef124bd4ceb2"
  },
  {
    "url": "next/api/permission.html",
    "revision": "8ea2e4b4a35d5c3914a9528affb2f55c"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "28a691e2eba1fa5821215ea0208018ae"
  },
  {
    "url": "next/api/rule.html",
    "revision": "38ac54e144003343d34977197b24b2d3"
  },
  {
    "url": "next/api/typing.html",
    "revision": "078fb36168c0eee43ecb083734bcfcb8"
  },
  {
    "url": "next/api/utils.html",
    "revision": "67c1860a550909191ad0bd1993ae5c57"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "5009d09f12fb8ef4b15dd01f7e22198a"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "315b3ae842abf2780aa7a9ffa6447b73"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "be908cc822aae2cf05d96aa5dfcccc02"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "ada80f887e95f0ba85112856e846a17d"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "8e1eac4dc22c8188cef8063be5b87465"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "050570e9f1bf1b81b9c3c37fe7fb7045"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "d019d511a21203353b933ee3007d6891"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "31765e1b9c0ea8f75bd6b2d86a49799f"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "2d15ad7cf413031a4720afb147581d7a"
  },
  {
    "url": "next/guide/index.html",
    "revision": "7085540ef532bfb3983797d2f3bf81db"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "8a6f64f3d1499cf1d8acfff931b729d2"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "7d68f6f349818b3ccc2c373c460c8a06"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "372fc067ad23794e679c2b9af1c0920f"
  },
  {
    "url": "next/index.html",
    "revision": "9de4dd633071bed15644be1287873bd8"
  },
  {
    "url": "store.html",
    "revision": "e36c79fcef8a10fc19654e65320def05"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
