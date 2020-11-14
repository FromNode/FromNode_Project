
  const secondBranch = async (data) => {
    createATag.setAttribute("class", `${data[0].pk}`); //처음 노드
    pkArray[0] = data[0].pk;
    for(let i = 1; i<data.length; i++){
        pkArray[i]=data[i].fields.previousCode;
    }
      for(let i = 0; i<data.length; i++){
          if(i==0){
            const firstTargetLocation = document.getElementsByClassName(`${data[0].pk}`)[0]; // 처음 노드
            const secondUl = firstTargetLocation.parentNode.appendChild(document.createElement("ul")); // 부모 요소 하위에 ul추가
            secondUl.classList.add(`branch${ulCreateCount}`); // class 선언
        } else if ( i > 0) {
            for(let k = 1; k < data.length; k++){
                if (data[k].fields.previousCode == data[0].pk){
                    let secondCreateText = document.createTextNode(`${data[k].pk}`);
                    let secondBranchNode = secondUl.appendChild(document.createElement("li")).appendChild(document.createElement("a"));
                    secondBranchNode.appendChild(secondCreateText);
                    secondBranchNode.setAttribute("class", `${data[k].pk}`);
                    pkArray[k] = 1;
                } else if (pkArray[i] == 1) {
                    const otherTargetLocation = document.getElementsByClassName(`${data[i].pk}`)[0];
                    const otherUl = otherTargetLocation.parentNode.appendChild(document.createElement("ul"));
                    otherUl.classList.add(`branch${ulCreateCount}`);
                    for(let k = 1; k < data.length; k++){
                        if(k != i && pkArray[k] != 1){
                        if(data[k].fields.previousCode == data[i].pk){
                            let otherCreateText = document.createTextNode(`${data[k].pk}`);
                            let otherBranchNode = otherUl.appendChild(document.createElement("li")).appendChild(document.createElement("a"));
                            otherBranchNode.appendChild(otherCreateText);
                            otherBranchNode.setAttribute("class", `${data[k].pk}`);
                            pkArray[k] = 1;
                        }
                        }
                    }

                }
            }
          } 
      }
      ulCreateCount++;
  }