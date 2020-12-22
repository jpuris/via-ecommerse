<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Store</h1>
        <hr><br><br>
        <alert :message="message" :messageVariant="messageVariant" v-if="showMessage"></alert>
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-outline-success btn-sm" @click="onSyncAllItems()">
            Sync all items
          </button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click="onDeleteAllItems()">
            Delete all items
          </button>
        </div>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">id</th>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Price</th>
              <th scope="col">Remaining</th>
              <th></th> <!-- button field -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in items" :key="index">
              <td >{{ item._id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.price }}</td>
              <td>{{ item.stock }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-outline-warning btn-sm"
                    @click="onOrderItem(item)">Order</button>
                  <button
                    type="button"
                    class="btn btn-outline-danger btn-sm"
                    @click="onSyncItem(item)">Sync</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {

      items: [],

      itemForm: {
        name: '',
        description: '',
        price: 0,
        stock: 0,
      },

      message: '',
      showMessage: false,
      messageVariant: 'success',

      api_url: `http://${process.env.VUE_APP_STORE_API_HOST}:${process.env.VUE_APP_STORE_API_PORT}`,
    };
  },

  components: {
    alert: Alert,
  },

  methods: {

    getItems() {
      const path = `${this.api_url}/api/v1/items/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    onSyncItem(item) {
      // eslint-disable-next-line
      this.syncItem(item._id);
    },
    syncItem(itemID) {
      const path = `${this.api_url}/api/v1/items/${itemID}/sync`;
      axios.post(path)
        .then((res) => {
          if (res.status === 205) {
            this.getItems();
            this.message = 'Item is already in sync!';
            this.messageVariant = 'warning';
            this.showMessage = true;
          } else {
            this.getItems();
            this.message = 'Item sync done!';
            this.showMessage = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Unable to sync the item!';
          this.showMessage = true;
        });
    },

    onOrderItem(item) {
      if (item.stock > 0) {
        // eslint-disable-next-line
        this.orderItem(item._id);
      } else {
        this.messageVariant = 'danger';
        this.message = 'Item is out of stock!';
        this.showMessage = true;
      }
    },
    orderItem(itemID) {
      const path = `${this.api_url}/api/v1/items/${itemID}/reserve?quantity=1`;
      axios.put(path)
        .then((res) => {
          if (res.status === 205) {
            this.getItems();
            this.message = 'Item is out of stock!';
            this.messageVariant = 'warning';
            this.showMessage = true;
          } else {
            this.getItems();
            this.messageVariant = 'success';
            this.message = 'Item has been reserved!';
            this.showMessage = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Unable to sync the item!';
          this.showMessage = true;
        });
    },

    onSyncAllItems() {
      // eslint-disable-next-line
      this.syncAllItems();
    },
    syncAllItems() {
      const path = `${this.api_url}/api/v1/items/sync`;
      axios.post(path)
        .then(() => {
          this.getItems();
          this.message = 'Sync done!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Unable to sync!';
          this.showMessage = true;
        });
    },

    onDeleteAllItems() {
      // eslint-disable-next-line
      this.deleteAllItems();
    },
    deleteAllItems() {
      const path = `${this.api_url}/api/v1/items/all`;
      axios.delete(path)
        .then(() => {
          this.getItems();
          this.message = 'items deleted!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Items failed to be deleted!';
          this.showMessage = true;
        });
    },
  },

  created() {
    console.log(this.api_url)
    this.getItems();
  },

};
</script>
