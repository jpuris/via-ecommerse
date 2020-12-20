<template>
  <div>
    <b-alert show dismissible :variant="messageVariant">{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message', 'messageVariant'],
};
</script>
