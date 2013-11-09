var app = angular.module('brochureApp', ['ngResource', 'ngSanitize', 'xeditable']);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

app.factory('productFactory', ['$http', function ($http) {
    var urlBase = '/';
    var productFactory = {};

    productFactory.query = function (url, store_name) {
        data = {'url': url, 'store_name': store_name};
        return $http.post(urlBase + 'query/', data);
    };

    productFactory.addItem = function (data, store_name) {
        data.store_name = store_name;
        return $http.post(urlBase + 'add_item/', data);
    };

    productFactory.getAll = function (store_name) {
        data = {'store_name': store_name};
        return $http.post(urlBase + 'get_items/', data);
    };

    productFactory.getWatchlist = function (store_name) {
        data = {'store_name': store_name};
        return $http.post(urlBase + 'get_watchlist/', data);
    };

    productFactory.deleteItems = function (selected) {
        return $http.post(urlBase + 'delete_items/', selected);
    };

    productFactory.dummy = function () {
        return $http.get(urlBase + 'sync/');
    };

    productFactory.setMark = function (data) {
        return $http.post(urlBase + 'set_mark/', data);
    };

    productFactory.updatePrice = function (data) {
        return $http.post(urlBase + 'update_price/', data);
    };

    return productFactory;
}]);

app.controller('brochureController', ['$scope', 'productFactory', function ($scope, productFactory) {
    var opts = {
            lines : 13, // The number of lines to draw
            length : 7, // The length of each line
            width : 4, // The line thickness
            radius : 10, // The radius of the inner circle
            corners : 1, // Corner roundness (0..1)
            rotate : 0, // The rotation offset
            color : '#000', // #rgb or #rrggbb
            speed : 1, // Rounds per second
            trail : 60, // Afterglow percentage
            shadow : false, // Whether to render a shadow
            hwaccel : false, // Whether to use hardware acceleration
            className : 'spinner', // The CSS class to assign to the spinner
            zIndex : 2e9, // The z-index (defaults to 2000000000)
            top : $(window).height()/2.5, // Manual positioning in viewport
            left : "auto"
    };
    productFactory.dummy();
    $scope.predicate = 'fields.current_price';
    $scope.reverse = false;
    $scope.info = 'Something is wrong.';
    $scope.itemClicked = function (store_name) {
        $('#addLink').hide();
        $('#addLinkNext').hide();
        $('#addLinkDetail').hide();
        $scope.store_name = store_name;
        $('.list-group-item').removeClass('active');
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.getAll(store_name).success(function (products) {
            productFactory.getWatchlist(store_name).success(function (watchlist) {
                for (var i = 0; i < products.length; i++) {
                    if (products[i].fields.error == true) {
                        products[i].fields.error_text = 'Error';
                    } else {
                        products[i].fields.error_text = products[i].fields.last_update;
                    }
                    for (var j = 0; j < watchlist.length; j++) {
                        if (products[i].pk === watchlist[j].fields.product) {
                            products[i].fields.desire_price = watchlist[j].fields.desire_price;
                            products[i].fields.mark = watchlist[j].fields.mark;
                        }
                    }
                }
            });
            $scope.spinner.stop();
            $scope.products = products;
        });
        $('#' + store_name +'List').addClass('active');
        $('#welcome').hide();
        $('#menubar').show();
        $('#hr').show();
        $('#table').show();
    };
    $scope.addLink = function () {
        $scope.info = 'Something is wrong.';
        $('#url').val('');
        $('#menubar').hide();
        $('#hr').hide();
        $('#table').hide();
        $('#addLink').show();
        $('#addLinkNext').show();
        $('#addLinkDetail').hide();
    };
    $scope.addLinkNext = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.query($scope.new.queryUrl, $scope.store_name).success(function (product) {
            $scope.spinner.stop();
            if (product.info != '') {
                $scope.info = product.info;
                $('#info').modal('show');
            } else {
                url = $scope.new.queryUrl;
                $scope.new = product;
                $scope.new.queryUrl = url;
                $('#addLinkNext').hide();
                $('#addLinkDetail').show();
            }
        }).error(function () {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
    $scope.submitProduct = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'url': $scope.new.queryUrl,
            'desire_price': $scope.new.desire_price,
            'current_price': $scope.new.current_price,
            'original_price': $scope.new.original_price,
            'name': $scope.new.name,
            'email': $scope.new.email,
            'uuid': $scope.new.uuid
        };
        productFactory.addItem(data, $scope.store_name).success(function (info) {
            productFactory.getAll($scope.store_name).success(function (products) {
                productFactory.getWatchlist($scope.store_name).success(function (watchlist) {
                    for (var i = 0; i < products.length; i++) {
                        if (products[i].fields.original_price == 0) {
                            products[i].fields.original_price = 'Unknown';
                        }
                        if (products[i].fields.error == true) {
                            products[i].fields.error_text = 'Error';
                        } else {
                            products[i].fields.error_text = products[i].fields.last_update;
                        }
                        for (var j = 0; j < watchlist.length; j++) {
                            if (products[i].pk === watchlist[j].fields.product) {
                                products[i].fields.desire_price = watchlist[j].fields.desire_price;
                                products[i].fields.mark = watchlist[j].fields.mark;
                            }
                        }
                    }
                });
                $scope.spinner.stop();
                $scope.products = products;
                $scope.spinner.stop();
            });

            $('#addLink').hide();
            $('#addLinkNext').hide();
            $('#addLinkDetail').show();
            $('#menubar').show();
            $('#hr').show();
            $('#table').show();
        });
    };
    $scope.selected = {};
    $scope.deleteItems = function () {
        for (pk in $scope.selected) {
            console.log(pk);
            console.log($scope.selected[pk]);
        }
        console.log($scope.selected);
        productFactory.deleteItems($scope.selected).success(function (info) {
            $scope.itemClicked($scope.store_name);
        });
    };
    $scope.selectAll = function () {
        console.log($('.selectAll').is(':checked'));
        if ($('.selectAll').is(':checked')) {
            for (var i = 0; i < $scope.products.length; i++) {
                $scope.selected[$scope.products[i].pk] = true;
            }
        } else {
            for (var i = 0; i < $scope.products.length; i++) {
                $scope.selected[$scope.products[i].pk] = false;
            }
        }
    };
    $scope.markClicked = function (pk) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
        }
        productFactory.setMark(data).success(function (info) {
            $scope.spinner.stop();
        });
    };
    $scope.updatePrice = function (pk, desire_price) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
            'desire_price': desire_price
        };
        productFactory.updatePrice(data).success(function (info) {
            $scope.spinner.stop();
        });
    }
}]);