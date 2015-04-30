requirejs.config({
    baseUrl: 'js',
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        jquery: 'jquery-2.1.3.min',
        knockout: 'knockout-3.3.0',
        kopunches: 'knockout.punches.min',
        pager: 'pager.min'
    }
});

requirejs(['jquery', 'knockout', 'kopunches', 'pager'], function($, ko, kopunches, pager) {
	function RootViewModel() {
		var self = this;
		self.user = ko.observable("User");

		self.getVM = function(path) {
			return function(callback) {
				requirejs(['/js/ko/viewmodels/'+path+'.js'], function(mod) {
					callback(mod);
				});
			};
		};
	}

	rootViewModel = new RootViewModel();

	pager.Href.hash = '#!/';

	pager.extendWithPage(rootViewModel);

	ko.punches.enableAll();

	ko.applyBindings(rootViewModel);

	pager.start();
});
