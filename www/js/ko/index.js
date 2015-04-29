function RootViewModel() {
	var self = this;
	self.user = ko.observable("User");
}

rootViewModel = new RootViewModel();

pager.extendWithPage(rootViewModel);

ko.punches.enableAll();

ko.applyBindings(rootViewModel);

pager.start();