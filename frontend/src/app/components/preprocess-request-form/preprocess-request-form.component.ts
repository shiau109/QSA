import {  
  Component,  
  Output,  
  EventEmitter  
} from '@angular/core';import { FormBuilder } from '@angular/forms';
import { PlotRequestTypesEnum, PlotRequestTypes2Label } from 'src/app/interfaces/data_extract'
import { ActivatedRoute } from '@angular/router';
import { Validators } from '@angular/forms';

@Component({
  selector: 'app-preprocess-request-form',
  templateUrl: './preprocess-request-form.component.html',
  styleUrls: ['./preprocess-request-form.component.css']
})
export class PreprocessRequestFormComponent {
  get_values = Object.values;
  show_CMD_hints:boolean;
  @Output() preProcessCMDs = new EventEmitter < Object > ();  

  req_form = this.fb.group({
    CMDs: '[]',
  });

  constructor(  private fb:FormBuilder,
                 ) {
    this.show_CMD_hints = false;
  }
  preProcess(): void{
    console.log('press preProcess button')
    let jsonObj = JSON.parse(this.req_form.value.CMDs!);
    console.log(jsonObj);
    this.preProcessCMDs.emit(jsonObj);  
  }
  click_help(): void{
    this.show_CMD_hints = !this.show_CMD_hints
  }
}
