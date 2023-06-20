import {Component, EventEmitter, Input, Output} from '@angular/core';

@Component({
  selector: 'app-validate-btn',
  templateUrl: './validate-btn.component.html',
  styleUrls: ['./validate-btn.component.scss']
})
export class ValidateBtnComponent {
  @Input() text: string = "validate Step";
  @Input() color: string = "primary";
  @Input() errorMessage: string = "";
  @Output() click: EventEmitter<any> = new EventEmitter;

}
