function getFunc() {
  ('[name=apimenu]').change(function() {
      // 選択されているvalue属性値を取り出す
      var val = $('[name=apimenu]').val();
      console.log(val); // 出力：ABC
      // 選択されている表示文字列を取り出す
      var txt = $('[name=apimenu] option:selected').text();
      console.log(txt); // 出力：えーびーしー
  });
        }
