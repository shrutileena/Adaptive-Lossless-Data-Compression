import { Component, OnInit } from '@angular/core';
import { SharedService } from '../services/shared.service';

@Component({
  selector: 'app-success',
  templateUrl: './success.component.html',
  styleUrls: ['./success.component.css']
})
export class SuccessComponent implements OnInit {
  len = 0;
  len_c = 0
  constructor(private shared: SharedService) { }

  ngOnInit(): void {
    this.len = this.shared.getLen();
    this.len_c = this.shared.getCompressedLen();
  }

}
