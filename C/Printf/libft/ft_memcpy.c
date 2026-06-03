/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 20:39:26 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/09 21:33:38 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
//#include <stddef.h>
#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*ptr1;
	const unsigned char	*ptr2;

	if (!src && !dest)
		return (NULL);
	ptr1 = (unsigned char *)dest;
	ptr2 = (const unsigned char *)src;
	i = 0;
	while (i < n)
	{
		ptr1[i] = ptr2[i];
		i++;
	}
	return (dest);
}

/*int	main(void)
{
	char *sourceArray = "Hello my name is Mustafa";
	char destinationArray[24];

    memcpy(destinationArray, sourceArray, 20);

    printf("Destination Array: ");
    for (int i = 0; i < 20; i++) {
        printf("%c", destinationArray[i]);
    }
    printf("\n");
}*/
