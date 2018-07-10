var igeClientConfig = {
	include: [
		/* Your custom game JS scripts */
		'/static/engine/maps/example.js',
		'/static/engine/gameClasses/ClientNetworkEvents.js',
		'/static/engine/gameClasses/Character.js',
		'/static/engine/gameClasses/PlayerComponent.js',
		'/static/engine/gameClasses/CharacterAi.js',
		/* Standard game scripts */
		'/static/engine/client.js',
		'/static/engine/index.js'
	]
};

if (typeof(module) !== 'undefined' && typeof(module.exports) !== 'undefined') { module.exports = igeClientConfig; }