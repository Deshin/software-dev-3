require(["/js/jquery-2.1.3.min.js", "/js/knockout-3.3.0.js", "/js/knockout.punches.min.js", "/js/pager.min.js"], function() {
	function RootViewModel() {
		var self = this;
		self.user = ko.observable("User");

		self.getVM = function(path) {
			return function(callback) {
				console.log('getting ' + '/js/ko/viewmodels/'+path+'.json');
				// $.getJSON('/js/ko/viewmodels/'+path+'.json', function(data) {
				// 	console.log('got it!');
				// 	console.log(data);
				// 	callback(data.getViewModel());
				// })
				// .done(function() {
				// 	console.log( "second success" );
				// })
				// .fail(function( jqxhr, textStatus, error ) {
				// 	var err = textStatus + ", " + error;
				// 	console.log( "Request Failed: " + err );
				// })
				// .always(function() {
				// console.log( "complete" );
				// });
				// LazyLoad.js("/js/ko/viewmodels/"+path+'.js', function() {
				// 	console.log(vm);
				// 	callback(vm);
				// });
				require(['/js/ko/viewmodels'+path+'.js'], function(mod) {
					callback(mod);
				});
			}
		}
	}

	rootViewModel = new RootViewModel();

	pager.Href.hash = '#!/';

	pager.extendWithPage(rootViewModel);

	ko.punches.enableAll();

	ko.applyBindings(rootViewModel);

	pager.start();
});