import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent {
  @Input() title?: string = undefined;
  @Input() type: 'hint' | 'secondary' | 'success' | 'error' | 'warning' | 'info' = 'hint';

  getTitle() : string {
    if (this.title == undefined) {
      this.title = this.type;
    }
    return this.title.charAt(0).toUpperCase() + this.title.slice(1);
  }
}
