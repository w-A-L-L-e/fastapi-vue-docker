<template>
  <div class="filedrop-wrapper">

    <div class="filedrop-box"
      :class="{'filedrop-box-dragover': isDragover}"
      @drop.prevent="dropHandler($event)"
      @dragover.prevent="setIsDragOver(true)"
      @dragleave.prevent="setIsDragOver(false)"
      v-if="!uploaded"
    >
      <label for="file-input" id="file-input-label">
        <span>{{ $t('upload_by_dropping_files') }}</span> <br/>
        <span class="smaller">
					{{ $t('or') }}	<strong><em>{{ $t('click_here') }}</em></strong> {{ $t('to_select_files') }}
        </span>
        <input type="file" id="file-input" multiple @change="onInputChange" />
			</label>
    </div>

    <div v-if="uploaded" class="upload-progress">
      <div class="circlewrap">
        <ProgressCircle :percent="getUploadPercentage()" /> 
      </div>
      <div class="progress-numbers">
        <p class="upload-percent"> {{getUploadPercentage()}} % </p>
        <p class="upload-filecount"> {{allFiles.length}} bestanden uploaden </p>
      </div>
    </div>
    <div class="clearfix"></div>


    <div class="file-box" v-for="f in allFiles" :key="f.name">
      <div class="file-name"> {{f.file.name}} </div>

      <div class="file-info"> 
        <span class="file-size">{{showSize(f.file.size)}} </span>
        <span class="upload-fail" v-if="f.status==false">
          {{ $t('error_during_uploading_file') }}
        </span>
        <span class="upload-status" v-if="f.status=='loading'">
          {{ $t('file_upload_busy') }}
        </span>
      </div>

      <div class="action-btn red" @click="deleteFile(f)">
        x
      </div>
    </div>

    <div class="footer">

      <label for="more-folders" id="more-folders-label">
       +  {{ $t('add_directory') }}
       <input type="file" id="more-folders" @change="onInputChange" webkitdirectory multiple />
      </label>

      <label for="more-files" id="more-files-label">
       +  {{ $t('add_more_files') }}
       <input type="file" id="more-files" @change="onInputChange" multiple />
      </label>
      
      <!-- we call uploadClicked using a ref instead
      <button 
        type="button" 
        id="upload-btn"
        class="btn btn-secondary"
        @click="uploadClicked">
          Uploaden &gt;
      </button>
      -->
    </div>

  </div>
</template>


<script>
  import axios from 'axios';
  import createUploader from '@/utils/file-uploader'
  import formatBytes from '@/utils/format-bytes'
  import ProgressCircle from '@/components/ProgressCircle.vue'


  export default {
    name: "FileDrop",
    components: {
      ProgressCircle
    },
    props: ['batch_id'],
    data () {
      return {
        //allFiles: File[] = [],
        allFiles: [],
        isDragover: false,
        uploading: false,
        uploaded: false
      }
    },
    methods: {
      deleteFile(file) {
        this.allFiles = this.allFiles.filter((f) => f !== file);
        if(this.allFiles.length == 0) this.uploaded=false;
      },

      dropHandler(event) {
        console.log("drophandler event=", event);
        const droppedFiles = event.dataTransfer.files;

        for(var i=0; i < droppedFiles.length; i++){
          let f = droppedFiles[i];
          this.allFiles.push(
            {
              'file': f,
              'status': 'dropped'
            }
          );
        }

        this.isDragover = false;
      },

      setIsDragOver(isDragover) {
        this.isDragover = isDragover;
      },

      onInputChange(e) {
        this.uploaded = false;
        const addedFiles = e.target.files;

        for(var i=0; i < addedFiles.length; i++){
          let f = addedFiles[i];
          this.allFiles.push(
            {
              'file': f,
              'status': 'selected'
            }
          );
        }

        e.target.value = null // reset so that selecting the same file again will still cause it to fire this change
      },

      redirectUploadComplete(){
        if(!this.allFiles.length) return;

        var no_errors=true;
        // todo iterate all files and only redirect
        // when no errors
        for(var i in this.allFiles){
          let file = this.allFiles[i];
          if(file.status == false){
            no_errors = false;
          }
          if(file.status == 'loading'){
            no_errors = false;
          }
        }

        if(no_errors){
          // wait a little for spinner animation to go to 100%
          setTimeout(()=>{
            this.uploading = false;
            this.$router.push('/batches/'+this.batch_id+'/upload_complete');
          }, 500);
        }
      },
      uploadClicked(){
        if(this.allFiles.length==0) return; //nothing to upload

        const { uploadFiles } = createUploader(
          axios.defaults.baseURL+'batches/'+this.batch_id+'/upload_essence' 
        )
        this.uploading = true;
        this.uploaded = true;
        uploadFiles(this.allFiles).then( () => {
          this.redirectUploadComplete()
        });
      },
      showSize(file_bytes){
        return formatBytes(file_bytes);
      },
      getUploadPercentage(){
        if(!this.allFiles) return 0;

        let total_files = this.allFiles.length
        if(total_files==0) return 0;

        let uploaded = 0.0;
        for(var i in this.allFiles){
          if(this.allFiles[i].status!='loading') uploaded += 1.0;
        }
        return Math.ceil((uploaded/total_files)*100);
      }
    }
  }
</script>

<style scoped>
  #file-input-label {
    padding: 10px 10px;
    margin-left: -50px;
    margin-right: -50px;
    font-size: 34px;
    cursor: pointer;
    width: 100%;
    border: 1px dashed;
    border-radius: 5px;
  }

  #file-input {
    display: none;
  }

  #more-files-label {
    display: inline-flex;
    cursor: pointer;
    margin-right: 20px;
  }
  #more-folders-label {
    display: inline-flex;
    cursor: pointer;
    margin-right: 20px;
  }

  #more-files{
    display: none;
  }

  #more-folders{
    display: none;
  }

  .filedrop-wrapper {
    text-align: center;
    margin-bottom: 70px;
  }
  .filedrop-box {
    background-color: #eee;
    margin-bottom: 20px;
    border-radius: 5px;
  }

  .filedrop-box-dragover {
    background-color: #ccc;
  }

  .file-box {
    border-bottom: 1px solid #ddd;
    padding: 5px;
    text-align: left;
  }

  .file-name{
    display: inline-flex;
    margin-right: 100px;
    font-weight: bold;
  }
  .file-info{
    color: #999;
  }
  .file-size{
    width: 40%;
    display: inline-block;
  }
 .upload-fail{
    color: #dd2222;
    margin-left: 10px;
  }
  .upload-status{
    color: #000;
    margin-left: 10px;
  }

  .action-btn {
    display: inline-flex;
    border: 1px solid #a22;
    background-color: #c22;
    color: #fff;
    padding-left: 7px;
    padding-right: 7px;
    border-radius: 7px;
    cursor: pointer;
    float: right;
    font-weight: bold;
    font-size: 13px;
    margin-top: -42px;
  }
  
  #upload-btn {
    float: right;
    margin-top: 1em;
  }

  .footer {
    margin-top: 20px;
    text-align: left;
  }

  .upload-progress {
    margin-top: 60px;
    text-align: left;
    height: 100px;
    margin-left: auto;
    margin-right: auto;
    width: 290px;
  }

  .upload-percent {
    font-size: 24px;
    font-weight: bold;
  }

  .upload-filecount{
    margin-top: -10px;
  }

  .circlewrap {
    float: left;
    margin-right: 20px;
  }

  .progress-numbers{
    float: left;
  }

 
</style>
