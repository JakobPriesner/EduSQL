import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {editor} from "monaco-editor";

@Component({
  selector: 'app-code-editor',
  templateUrl: 'code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit {
  @Output() onCodeChangeEvent: EventEmitter<string> = new EventEmitter<string>();

  editorOptions = {theme: 'vs-dark', language: 'sql', automaticLayout: true};
  code: string = '';
  editor: editor.IStandaloneCodeEditor | undefined = undefined;

  ngOnInit(): void {
  }

  onCodeChange(event: string) : void {
    this.onCodeChangeEvent.emit(event);
  }

  onEditorInit(editor: editor.IStandaloneCodeEditor) {
    this.editor = editor;
    console.log(this.editor);
    editor.layout();
  }


}
