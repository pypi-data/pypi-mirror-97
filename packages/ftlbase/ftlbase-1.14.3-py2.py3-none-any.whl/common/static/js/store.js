

var ROUTING = (function(){
    var self = {};

    self.init = function(server,csrftoken){
        self.server = server;
        self.csrftoken = csrftoken || {};

        self.routes = {
            banco: {
                create: `${self.server}/api/banco`,
                show: `${self.server}/api/banco`,
                update(id){
                    return `${self.server}/api/banco/${id}`
                },
                delete(id){
                    return `${self.server}/api/banco/${id}`
                },
                getById(id){
                    return `${self.server}/api/banco/${id}`
                },

            }
        }

    }

    return self;

})();

var UTIL = (function(router){
    self = {};
    self.packageData = function(data){
        contents = {csrfmiddlewaretoken:router.csrftoken};
        for (var key in data){
            contents[key] = data[key];
        }
        return contents;
    }
    return self;
})(ROUTING);

var BANCO = (function(router,helper){
    var self = {};

    self.show = function(){
        url = router.routes.banco.show;
        return $.get(url);
    }

    self.create = function(data){
        url = router.routes.banco.create;
        data = helper.packageData(data);
        return $.post(url,data);
    }

    self.update = function(id,data){
        // url = router.routes.banco.update(id)
        // data = helper.packageData(data)
        // return $.post(url,data)
        // console.log('Update:',data)
        return client.banco.update(id, data);
    }

    self.delete = function(id){
        url = router.routes.banco.delete(id);
        data = helper.packageData({});
        return $.delete(url,data);
    }

    self.getById = function(id){
        url = router.routes.banco.getById(id);
        data = helper.packageData({});
        return $.get(url,data);
        //return client.banco.read(id);
    }

    self.findById = function(id,objArray){
        for (var i in objArray){
            ob = objArray[i];
            if (ob.codigoCompensacao === id) {
                return ob;
            }
        }
        return false;
    }

    return self;

})(ROUTING,UTIL);


var STORE = (function(){
    // private
    var self = {};

    self.init = function(server,token){
        ROUTING.init(server,token);
        self.bancoUrl = `${server}/api/banco/`;
    }

    function STORE(server,token){
        self.init(server,token);
        this.routes = ROUTING;
        // modules
        this.banco = BANCO;

        // methods
        this.findById = function(id,objArray){
            for (var i in objArray){
                task = objArray[i];
                if (task.id === id) {
                    return task;
                }
            }
            return false;
        }

        this.findAndDelete = function(items,id){
            for(var i =0; i< items.length;i++){
                if (items[i].id === id){
                    items.splice(i, 1);
                    return true;
                }
            }
            return false;
        }

        // end functions
    }
    return STORE;
})(BANCO,ROUTING);

