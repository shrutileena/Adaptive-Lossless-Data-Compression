import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AldcService } from '../services/aldc.service';
import { SharedService } from '../services/shared.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  title = 'ALDC-website';
  file:File = null;
  
  constructor(private api:AldcService, private router: Router, private shared: SharedService) {  }

  onChange(event) {
    this.file = event.target.files[0];
  }

  onUpload() {
    console.log('submitting...')
    this.api.compress(this.file).subscribe((event) => {
      console.log(event['done']);
      if(event['done'] === true) {
        this.shared.len = event['len'];
        this.shared.len_c = event['len_c'];
        this.router.navigate(['/success']);
      }
    },(error)=> {
      console.log(error.message);
    })
  }

}
