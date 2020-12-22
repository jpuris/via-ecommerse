<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Warehouse</h1>
        <hr><br><br>
        <alert :message="message" :messageVariant="messageVariant" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.item-modal>Add Item</button>
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
                  >Update</button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteItem(item)"
                  >Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addItemModal" id="item-modal" title="Add a new item" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="itemForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-description-group"
                      label="Description:"
                      label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="itemForm.description"
                        required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="text"
                        v-model="itemForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-stock-group"
                      label="Stock:"
                      label-for="form-stock-input">
          <b-form-input id="form-stock-input"
                        type="text"
                        v-model="itemForm.stock"
                        required
                        placeholder="Enter remaining stock">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="editItemModal"
             id="item-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-group"
                      label="Name:"
                      label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="itemForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-description-group"
                      label="Description:"
                      label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="itemForm.description"
                        required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="text"
                        v-model="itemForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-stock-group"
                      label="Stock:"
                      label-for="form-stock-input">
          <b-form-input id="form-stock-input"
                        type="text"
                        v-model="itemForm.stock"
                        required
                        placeholder="Enter remaining stock">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

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

      api_url: `http://${process.env.VUE_APP_WH_API_HOST}:${process.env.VUE_APP_WH_API_PORT}`,
    };
  },

  components: {
    alert: Alert,
  },

  methods: {

    initForm() {
      // eslint-disable-next-line
      this.itemForm._id = '';
      this.itemForm.name = '';
      this.itemForm.description = '';
      this.itemForm.price = 0;
      this.itemForm.stock = 0;
    },

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

    addItem(payload) {
      const path = `${this.api_url}/api/v1/items/`;
      axios.post(path, payload)
        .then(() => {
          this.getItems();
          this.messageVariant = 'success';
          this.message = 'Item added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Item was not added!';
          this.showMessage = true;
        });
    },

    editItem(item) {
      this.itemForm = item;
    },

    updateItem(payload, itemID) {
      const path = `${this.api_url}/api/v1/items/${itemID}`;
      axios.put(path, payload)
        .then(() => {
          this.getItems();
          this.messageVariant = 'success';
          this.message = 'Item updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getItems();
          this.messageVariant = 'danger';
          this.message = 'Item was not updated!';
          this.showMessage = true;
        });
    },

    removeItem(itemID) {
      const path = `${this.api_url}/api/v1/items/${itemID}`;
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
    onDeleteItem(item) {
      // eslint-disable-next-line
      this.removeItem(item._id);
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addItemModal.hide();
      const payload = {
        name: this.itemForm.name,
        description: this.itemForm.description,
        price: this.itemForm.price,
        stock: this.itemForm.stock,
      };
      this.addItem(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addItemModal.hide();
      this.initForm();
    },

    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editItemModal.hide();
      const payload = {
        name: this.itemForm.name,
        description: this.itemForm.description,
        price: this.itemForm.price,
        stock: this.itemForm.stock,
      };
      // eslint-disable-next-line
      this.updateItem(payload, this.itemForm._id);
    },

    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editItemModal.hide();
      this.initForm();
      this.getItems(); // why?
    },
  },

  created() {
    this.getItems();
  },

};
</script>
