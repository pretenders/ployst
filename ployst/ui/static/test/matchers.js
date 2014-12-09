beforeEach(function() {
    this.addMatchers({
        toNgEqual: function(expected) {
            return angular.equals(this.actual, expected);
        }
    });
});
