import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-code-editor',
  templateUrl: 'code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit {
  @Output() onCodeChangeEvent: EventEmitter<string> = new EventEmitter<string>();

  editorOptions = {theme: 'vs-dark', language: 'sql'};
  code: string = '';

  ngOnInit(): void {
  }

  onCodeChange(event: string) : void {
    this.onCodeChangeEvent.emit(event);
  }
}
