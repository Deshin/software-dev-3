function RootViewModel() {
	var self = this;
	self.user = ko.observable("User");

	self.getVM = function(path) {
		return function(callback) {
			console.log('getting ' + '/js/ko/viewmodels/'+path+'.json');
			$.getJSON('/js/ko/viewmodels/'+path+'.json', function(data) {
				console.log('got it!');
				console.log(data);
				callback(data.getViewModel());
			})
			.done(function() {
				console.log( "second success" );
			})
			.fail(function( jqxhr, textStatus, error ) {
				var err = textStatus + ", " + error;
				console.log( "Request Failed: " + err );
			})
			.always(function() {
			console.log( "complete" );
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