"""
YesPDF

O módulo YesPDF tem como objetivo automatizar processos de coleta
de texto pelo Python.
"""

from typing import overload, Self, Optional, List, Tuple
import pymupdf
import os

__all__ = ["ypdf"]

class _ypdfBase:
    def __init__(
        self,
        arg: Optional[str] = None,
        ) -> Self:
        self.arg = arg 
    def _ispdf(self) -> bool:
        return self.arg.endswith('.pdf') if self.arg else False

    def _numpages(self) -> int:
        with pymupdf.open(self.arg) as pdf:
            return len(pdf) if pdf else 0
                    
    def _name(self) -> Optional[str]:
        return os.path.basename(self.arg) if self.arg else None

    def _fullname(self) -> Optional[str]:
        return os.path.abspath(self.arg) if self.arg else None

    def _text(self) -> Optional[str]:
        text: str = ""
        with pymupdf.open(self.arg) as _doc:
            text = chr(12).join([page.get_text(sort=True) for page in _doc])
        return text if text else None

    def _splittext(self, index: bool = False) -> Optional[List[tuple[int, str]] | List[str]]:
        text: str = self._text()
        if isinstance(text, str):
            _lines = text.splitlines()
            if index:
                return [(i, line) for i, line in enumerate(_lines)]
            return _lines
        return None

class ypdf(_ypdfBase):
    def __init__(
        self,
        document: Optional[str] = None
        ) -> Self:
        super().__init__(document)
        self.document = document
    @property
    def ispdf(self) -> bool:
        """Verifica se um parâmetro é um PDF.
        
            obj.ispdf

        Se terminar com '.pdf' retorna True, caso contrário
        retorna False.
        """
        return self._ispdf()
    @property
    def numpages(self) -> int:
        """Armazena a quantia de páginas do PDF.
        
            obj.numpages

        Retorna um inteiro, caso não encontre nenhuma
        página será retornado 0 (zero).
        """
        return self._numpages()
    @property
    def name(self) -> Optional[str]:
        """Armazena o caminho base do documento.
        
            obj.name

        Retorna o basename do documento, caso não encontre
        o path, retorna None.
        """
        return self._name()
    @property
    def fullname(self) -> Optional[str]:
        """Armazena o caminho absoluto do documento.
        
            obj.fullname

        Retorna o abspath do documento, caso não encontre
        o path, retorna None.
        """
        return self._fullname()
    @property
    def text(self) -> Optional[str]:
        """Armazena o texto do PDF.
        
            obj.text

        Retorna uma string do PDF, caso seja vazio
        é retornado None.
        """
        return self._text()
    @overload
    def splittext(self) -> Optional[List[str]]: ...
    @overload
    def splittext(self, index: bool) -> Optional[List[Tuple[int, str]]]: ...

    def splittext(self, index: Optional[bool] = None) -> Optional[List[str] | List[Tuple[int, str]]]:
        """Armazena o texto do PDF em uma lista ou tupla com index.
        
            obj.splittext() or obj.splittext(index=False)
            obj.splittext(index=True)
            
        Retorna uma lista de cada linha quebrada do PDF, caso
        o argumento index=True seja parseado, retorna uma tupla
        enumerando cada linha.
        """
        if index is None: return self._splittext(index=False)
        else: return self._splittext(index=index)