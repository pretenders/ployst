beforeEach(function() {

    var ngEquals = function(actual, expected) {
        var result = {
            pass: angular.equals(actual, expected)
        };
        return result;
    };

    jasmine.addMatchers({
        toNgEqual: function() {
            return {
                compare: ngEquals
            };
        }
    });
});
