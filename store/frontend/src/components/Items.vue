<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Store</h1>
        <hr><br><br>
        <alert :message="message" :messageVariant="messageVariant" v-if="showMessage"></alert>
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-success btn-sm" v-b-modal.item-modal>
            Sync all items
          </button>
          <button type="button" class="btn btn-danger btn-sm" @click="onDeleteAllItems()">
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
              <td>{{ item._id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.price }}</td>
              <td>{{ item.stock }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.item-update-modal
                    @click="editItem(item)"
                  >Order</button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onSyncItem(item)"
                  >Sync</button>
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
    };
  },

  components: {
    alert: Alert,
  },

  methods: {

    getItems() {
      const path = 'http://localhost:8100/api/v1/items/';
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    syncItem(itemID) {
      const path = `http://localhost:8100/api/v1/items/${itemID}`;
      axios.delete(path)
        .then(() => {
          this.getItems();
          this.message = 'Item removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Item was not removed!';
          this.showMessage = true;
        });
    },
    onSyncItem(item) {
      // eslint-disable-next-line
      this.syncItem(item._id);
    },

    deleteAllItems() {
      const path = 'http://localhost:8100/api/v1/items/all';
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
    onDeleteAllItems() {
      // eslint-disable-next-line
      this.deleteAllItems();
    },
  },

  created() {
    this.getItems();
  },

};
</script>
